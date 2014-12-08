
CHARTS by Brace
---------------

Make charts in seconds

Use our URL to inject charts into your website. The data is supplied via the URL, no Javascript required. Plus, if you need Lorem Ipsum charts, we've got you covered.

Example:

    <img src="//charts.brace.io/bar.svg?Foo=1,1,2,3,5">


### Pies, Bars and Lines

There are 3 different types of charts. Choose one by changing the path.

#### Pies

    charts.brace.io/pie.svg?Things=5&Stuff=2

#### Bars

    charts.brace.io/bar.svg?Things=lorem_exp

#### Lines

    charts.brace.io/line.svg?Things=lorem_flat

### Choose a Style

Just by adding _style=Stylename to the URL

#### Light (default)

    charts.brace.io/bar.svg?Foo=lorem_exp&_style=light

#### Dark

    charts.brace.io/bar.svg?Foo=lorem_exp&_style=dark

### Supplying data

You can just append the data for the chart to the URL parameters.

#### Bars and Lines

Generally you provide DataSet=<list-of-values>. For example:

    charts.brace.io/line.svg?Things=1,2,3

You can also have multiple datasets, like:

    charts.brace.io/line.svg?Some=1,2,3&Thing=2,3,4

Finally, you can add labels to the x axis:

    charts.brace.io/bar.svg?Likes=3,2,4&_labels=Jan,Feb,Mar

#### Pies

For pies it's mostly the same, except you have names for sections and one value per section.

    charts.brace.io/pie.svg?Some=1&Thing=2

### Other fancy features

Here are some additional neat features that Brace Charts provide.

#### Generate placeholder data

If you're prototyping and need placeholder charts, we have a solution for you. Instead of providing numbers, you can just use one of these keywords.

    charts.brace.io/bar.svg?Stuff=lorem_exp

    charts.brace.io/bar.svg?Stuff=lorem_hockey

    charts.brace.io/bar.svg?Stuff=lorem_bell

    charts.brace.io/bar.svg?Stuff=lorem_flat

#### Customize the appearance of (line) charts

    <img src="http://charts.brace.io/line.svg?Foo=lorem_hockey&_show_legend=false&_height=300px&_interpolate=cubic&_fill=true">

#### Show off with hover effects

Use an <object> tag instead of images. This gives you fancy hover-states.

    <object type="image/svg+xml" data="http://charts.brace.io/line.svg?Some=lorem_flat&Stuff=lorem_flat&_interpolate=cubic &_fill=true&_height=300px"></object>

### Questions you might have

#### How much does it cost?

For now, Brace Charts is free and is limited to 10,000 views per chart per month. If you need more, please reach out to team@brace.io.

#### What charting library did you use?

Brace Charts is based on pygal, an awesome charting library for Python.

#### Who are you guys?

We're the same folks who make Brace.io, the simple way to host websites. Brace Charts is one of our sideprojects that aim to make authoring and designing for the web easy.

--------

Brace Charts is a tool made by Brace.io. To contact us send an email to team@brace.io or use the form on the right.

Other stuff we've made

Brace.io is the easiest way to host websites via Dropbox

Formspree provides forms for static sites. No PHP, Javascript or iFrames required.
   SEND
  
