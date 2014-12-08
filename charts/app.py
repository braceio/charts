import flask
from flask import request, url_for, render_template, redirect, Response
# from paste.util.multidict import MultiDict
import json
import settings
import log
import os
import hashlib
import urlparse
import re

import redis
import pygal
from pygal import style

import loremdata

TEMPPATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates')
CHARTCSS = os.path.join(TEMPPATH, 'chartbase.css')
REDIS = redis.Redis.from_url(settings.REDIS_URL)
COUNTER_KEY = lambda x: 'charts_domain_counter_%s' % x
CHART_KEY = lambda x: 'charts_chart_counter_%s' % x

def _loads(val):
    '''
    Loads a string and returns a python datastructure. It ultimately calls
    json.loads() but handles some exceptions:

    - [] aren't needed around lists
    - list items can use single quotes
    - unquoted list items that don't evaluate to json objects are first
      wrapped in quotes

    Doesn't attempt to do anything smart with nested data structures or
    dictionaries.
    '''
    def _b(val): return u"["+val+u"]"

    try:
        return json.loads(val)
    except ValueError:
        # try converting quotes
        try:
            val = val.replace(u"'", u'"')
            return json.loads(val)
        except ValueError:
            # try brackets
            try:
                return json.loads(_b(val))
            except ValueError:
                # try brackets and quoting elements
                try:
                    parts = val.split(u",")
                    if len(parts) > 1:
                        testval = _b(u",".join([u'"'+p+u'"' for p in parts]))
                        return json.loads(testval)
                    return val
                except ValueError:
                    return val


def renderchart(kind):

    # get chart kind

    try:
        chartnames = [n.lower() for n in pygal.graph.CHARTS_NAMES]
        name_idx = chartnames.index(kind.lower())
    except ValueError:
        name_idx = 0

    chart_kind = getattr(pygal, pygal.graph.CHARTS_NAMES[name_idx], pygal.Line)

    # get arguments and series data

    configs = dict((key[1:],_loads(val)) for key,val in request.args.items() if key.startswith('_'))
    series = dict((key,val) for key,val in request.args.items() if not key.startswith('_'))

    # set configs

    if 'style' in configs:
        if configs['style'].lower() == "dark":
            configs['style'] = style.DefaultStyle
        else:
            try:
                styles = [n.lower() for n in dir(style) if n.endswith('Style')]
                style_idx = styles.index(configs['style'].lower())
                configs['style'] = getattr(style, dir(style)[style_idx])
            except ValueError:
                del configs['style']

    if 'labels' in configs and not 'x_labels' in configs:
        if type(configs['labels']) == list:
            configs['x_labels'] = [unicode(x) for x in configs['labels']]

    if 'width' in configs and type(configs['width']) in [str, unicode]:
        try:
            configs['width'] = json.loads(configs['width'].replace(u'px', u''))
        except:
            pass

    if 'height' in configs and type(configs['height']) in [str, unicode]:
        try:
            configs['height'] = json.loads(configs['height'].replace(u'px', u''))
        except:
            pass

    custom_style = style.Style(
      background='transparent',
      plot_background='rgba(0,0,0,0)' if kind.lower() == 'sparkline' else 'rgba(0,0,0,0.05)',
      foreground='#000',
      foreground_light='#000',
      foreground_dark='#000',
      colors=(
        'rgb(12,55,149)', 'rgb(117,38,65)', 'rgb(228,127,0)', 'rgb(159,170,0)',
        'rgb(149,12,12)')
      )

    params = {
        'label_font_size':18,
        'major_label_font_size':18,
        'legend_font_size':24,
        'title_font_size':24,
        'show_y_guides':False,
        'show_x_guides':False,
        'print_values':False,
        'y_labels_major_count':3,
        'show_minor_y_labels':False,
        'style':custom_style,
    }

    params.update(configs)
    config = pygal.Config(no_prefix=True, **params)
    config.css.append(CHARTCSS)

    # write out chart

    chart = chart_kind(config)
    for key, val in series.items():
        try:
            parsed = _loads(val)
            if type(parsed) in [str,unicode] and parsed.lower().startswith(u'lorem_'):
                chart.add(key, loremdata.loremdata(parsed))
            else:
                chart.add(key, _loads(val))
        except ValueError:
            pass

    if kind.lower() == 'sparkline':
        rendered = chart.render_sparkline()
    else:
        rendered = chart.render()

    # tracking

    if request.referrer:
        try:
            rparse = urlparse.urlparse(request.referrer)
            rhost = re.sub(r"\W", "_", rparse.netloc)
        except:
            rhost = re.sub(r"\W", "_", request.referrer.split(u"://")[1])
        REDIS.incr(COUNTER_KEY(rhost))

    charturl = re.sub(r"\W", "_", request.url.split(u"://")[1])
    REDIS.incr(CHART_KEY(charturl))

    return Response(rendered, mimetype='image/svg+xml')


def print_stats():
    print("Domains ---------------")
    domains = []
    for k in REDIS.keys(COUNTER_KEY(u'*')):
        if not k.startswith(COUNTER_KEY(u'reloaderdraft')):
            domains.append((k.replace(COUNTER_KEY(u''),u''), int(REDIS.get(k))))
    for i, v in enumerate(sorted(domains, key=lambda x: x[1])):
        print("%4d: %s, %d" % (i, v[0].replace(u'_',u'.'), v[1]))

    # print("Charts ----------------")
    # charts = []
    # for k in REDIS.keys(CHART_KEY(u'*')):
    #     charts.append((k, int(REDIS.get(k))))
    # for i, v in enumerate(sorted(charts, key=lambda x: x[1])):
    #     print("%4d: %s, %d" % (i, v[0], v[1]))


def index():
    return flask.render_template('index.html', is_redirect=request.args.get('redirected'))


def favicon():
    return flask.redirect(url_for('static', filename='img/favicon.ico'))


def configure_routes(app):
    app.add_url_rule('/', 'index', view_func=index, methods=['GET'])
    app.add_url_rule('/favicon.ico', view_func=favicon)
    app.add_url_rule('/<kind>.svg', 'send', view_func=renderchart, methods=['GET'])


def create_app():
    app = flask.Flask('charts')
    app.config.from_object(settings)
    configure_routes(app)

    @app.errorhandler(500)
    def internal_error(e):
        return render_template('500.html'), 500

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error.html', title='Oops, page not found'), 404

    app.jinja_env.filters['nl2br'] = lambda val: val.replace('\n','<br>\n')
    
    return app