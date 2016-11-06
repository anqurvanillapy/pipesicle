postocol
========

**Posting Protocol**, SSG (static site generator) abstract class for extensible
use. Only supports Python 3.5+, for the compatibility of 3.4, 2.7 or other
versions not tested and guaranteed.

Requirements
------------

- [Jinja2](http://jinja.pocoo.org/) `>=2.8`
- [Markdown](https://pythonhosted.org/Markdown/) `>=2.6.7`
- [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/) `>=4.5.1`
- [Pygments](http://pygments.org/) `>=2.1.3`

Installation
------------

Not on PyPI yet. Please clone and manually run the setup script.

```bash
$ git clone git@github.com:anqurvanillapy/postocol.git
$ cd postocol
$ python3 setup.py install # or use `-r` to specify requirements
```

Implementation Workflow
-----------------------

- There are **3** document types that Postocol mainly serves, which are:
    + Single page (e.g. slideshow)
    + Blog
    + Wiki
- Therefore, Postocol will by default trace **6** types of templates as follows:
    + `index`, for blog or wiki, or even the slideshow (because it can be stored
    in one static HTML file, hence assuming that it is an index page)
    + `post`, for blog or wiki, e.g. an article
    + `states`, mainly for wiki, a list containing the current states of a post,
    e.g. *unfinished*, *not proofread*, *stub*, etc., similar to
    [Wikipedia:Tagging pages for problems](https://en.wikipedia.org/wiki/Wikipedia:Tagging_pages_for_problems)
    + `properties`, for wiki or blog, a list of the properties of a post, e.g.
    *howto*, *daily*, *compsci*, *PoC*, etc., similarly the categories or tags
    + `misc`, something you want to provide independently, instead of listing in
    `index`, `states` or `properties`, e.g. *about*, *contact*, *resume*, etc.
    + `layout`, serving something above
- **Additionally**, `index`, `states` and `properties` could be automatically
generated from self-implemented `Postocol.render()` method.

### For single-page (slideshow) generator

There is no need to `clean()` anything and `send_static()` for a single-page
generator, so the workflow is simple. For instance, a slideshow generator might
act like this.

```
                    load_templates()     publish()
                          |                  |
                          v                  v
(slides.md) --+------- template ---+--> (index.html)
              |                    |
              +-- post ---> page --+
                   ^          ^
                   |          |
            load_posts()   render()
```

### For blog/wiki generator

Wiki uses the whole functionality to update all the posts, whereas the workflow
of a blog generator is similar:

```
(foo.md) --+
(bar.md) --+  clean(site/)  load_templates()  publish()  send_static()
           |         |            |              |             |
           v         v            v              v             v
       (content/) ---+----- templates ---+--> (site/) --+-> (site/static/)
                     |                   |              +-- (index.html)
                     +-- posts -> pages -+              +-- (states.html)
                          ^         ^                   +-- (properties.html)
                          |         |                   +-- (foo.html)
                   load_posts()  render()               +-- (bar.html)
```

API Reference
-------------

### Properties

#### `ifpath`

|Type|Default|
|:-:|:-:|
|`str`|`'content'`|

Input file/directory.

#### `ofpath`

|Type|Default|
|:-:|:-:|
|`str`|`'site'`|

Output file/directory.

#### `tmplpath`

|Type|Default|
|:-:|:-:|
|`str`|`'templates'`|

Template directory, mainly used by `jinja2.Environment` with the loader
`jinja2.FileSystemLoader` for better flexibility.

#### `staticpath`

|Type|Default|
|:-:|:-:|
|`str`|`'static'`|

Static assets directory.

#### `default_post_type`

|Type|Default|
|:-:|:-:|
|`str`|`'post'`|

If a post contains no `type`'s in meta, insert `default_post_type` into it when
the method `Postocol.load_posts()` is executed, for the convenience in someone's
writing the post.

#### `pymd_exts`

|Type|Default|
|:-:|:-:|
|`list`|`['markdown.extensions.meta']`|

List of needed
[python-markdown extensions](https://pythonhosted.org/Markdown/extensions/index.html),
where the "Name" suffixes should be given and will be completed, e.g. pass a
`['extra']` and it will be extended to `['markdown.extensions.extra']` in the
background.

### `Postocol.clean()`

|Argument|Return|
|:-:|:-:|
|Void|Void|

Clean all the files with extensions `.html` or `.htm` in the directory `ofpath`,
and it will not remove anything if `ofpath` is a file.

### `Postocol.load_templates(fpath=None)`

|`fpath` Type|Return Type|
|:-:|:-:|
|`str`; `self.tmplpath` by default|`dict`|

Load all [valid templates](#implementation-workflow) from `fpath`, and return a
dict with the valid template types as keys, and the Jinja2 template paths as
values. **Attention, the template file extension should only be `.html`.**

### `Postocol.load_posts(fpath=None)`

|`fpath` Type|Return Type|
|:-:|:-:|
|`str`; `self.ifpath` by default|`list`|

Load all valid Markdown posts from `fpath`, and return a list of their paths.
These extensions are only readable for this method: `.markdown`, `.mdown`,
`.mkdn`, `.md`, `.mkd`, `.mdwn`, `.mdtxt`, `.mdtext`, `.text` and `.txt`.

### `Postocol.render(posts)` (**abstract**)

|`posts` Type|Return Type|
|:-:|:-:|
|`list`|`list`|

Abstract method for rendering the loaded Markdown posts. You can use
[bs4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) and
[python-markdown](https://pythonhosted.org/Markdown/) to implement the
rendering, but **most importantly, returned list of pages (a page is a dict)
should have at least 3 keys,** which are `content` (Markdown-generated stuff),
`meta` (metadata of a post) and `fname` (outpuf filename).

For example, a valid returned `pages` dict looks like this:

```python
pages = [{'content': '<p>Rendered paragraph</p>',
          'meta': {'title': ['Hello, Postocol!'],
                   'type': ['post']},
          'fname': 'foo.html'}]
```

### `Postocol.publish(pages, tmpls)`

|`pages` Type|`tmpls` Type|Return|
|:-:|:-:|:-:|
|`list`|`dict`|Void|

Render the templates `tmpls` with the generated HTML `pages`, and write them
to `ofpath`. If `ofpath` is a file, the `fname` value in a page dict will be
overridden, and the method brings out the file `ofpath`.

### `Postocol.send_static(dest)`

|`dest` Type|Return|
|:-:|:-:|
|`str`|Void|

Send the static assets directory `self.staticpath` to the `dest` directory,
which might store some stylesheets, scripts or images. 

### `Postocol.create_page_dict(content, tmpl_type)`

|`content` Type|`tmpl_type` Type|Return Type|
|:-:|:-:|:-:|
|`str`, `list` or `dict`|`str`|`dict`|

Create a page dict manually, especially for `index`, `states` or `properties`
because they could be automatically generated by self-implemented `render()`
method. For instance, `content` can be a list of posts' titles and filenames,
and pass `'index'` to argument `tmpl_type`, and what will be returned is a
dict like:

```
{
    'content': [{'title': 'Foo', fname': 'foo.html'}],
    'meta': {'type': ['index']},
    'fname': 'index.html'
}
```

And this is valid for `publish()` to render the templates. For further example
about how to autogenerate an `index` (or `states`, etc.), please check out the
[examples](https://github.com/anqurvanillapy/postocol/tree/master/examples)
directory, where there is a wiki generator.

### `Postocol.send_codehilite_style(theme, dest)`

|`theme` Type|`dest` Type|Return|
|:-:|:-:|:-:|
|`str`; `'default'` by default|`str`; `self.staticpath` by default|Void|

Create a [pygments.styles](http://pygments.org/docs/styles/) stylesheet with
CSS class name `.codehilite` for the use of `python-markdown`'s extension,
[codehilite](https://pythonhosted.org/Markdown/extensions/code_hilite.html).
Checkout the example of the wiki generator for more details.

Examples
--------

### Starter

The project site hosted on
[gh-pages branch](https://github.com/anqurvanillapy/postocol/tree/gh-pages)
contains a minimalist webpage generator that ignores two unnecessary methods
`clean()` and `send_static()`, which can be your first sight under the hood.

> Off we go!

First, import everything we need to implement our own `render()` method. `os`
module can help us modify the filenames in the following steps. In the meantime,
create a class inheriting `Postocol` with some key constants.

```python
from postocol import Postocol
from os.path import basename, splitext


class Starter(Postocol):
    ifpath = 'preface.md'
    ofpath = 'index.html'
```

Second, we add a `run()` method for the control flow, which goes like

> Load templates from `templates` folder, and load `preface.md` to a list called
`posts`. Render the Markdown file and bring the `pages` out. Phew, finally, we
can publish it to the file `index.html` right now, which is combined with our
`templates` and `pages`.

```python
def run(self):
    self.tmpls = self.load_templates()
    self.posts = self.load_posts()
    self.pages = self.render(self.posts)
    self.publish(self.pages, self.tmpls)
```

Eventually, here comes the boss! Now implement the abstract method `render()` to
extract the list of posts tuples to do some manipulation, and pass it to our
pages list. `Postocol.load_posts()` collects **3** kinds of the page data:
`content` (the generated HTML content), `meta` (title, type, date,
etc., right at the beginning of a Markdown post) and `fname` (filename). Since
we don't need to do something like auto-generating a table of contents in index,
we now can straightly pass them to the page list.

```python
def render(self, posts):
    pages = []
    # Tiny function to extract the filename and add a `.html` extension
    chfn = lambda x: '{}.html'.format(splitext(basename(x))[0])

    for c, m, f in posts:
        # Jinja2 renders the templates using kwargs, hence `pages` is a list
        # of the dicts
        pages.append({'content': c, 'meta': m, 'fname': chfn(f)})

    return pages
```

What is inside the `preface.md` and the index template will not be displayed
right here. Check out the
[branch](https://github.com/anqurvanillapy/postocol/tree/gh-pages), where the
generator uses `Postocol.send_codehilite_style()` to create code highlighting
stylesheet for the code snippets. Run the script to see what magic will happen!

### Main Course

See [examples](https://github.com/anqurvanillapy/postocol/tree/master/examples)
directory that offers a fully implemented **wiki** generator demo, which may
help you fast-prototyping your own generator.

Test
----

Postocol doesn't use any third-party testing libraries, for the built-in
`unittest` is decent for testing its basic functionality, which is able to be
used from the command line.

```bash
$ python3 -m unittest # use `-v` to show verbose of the test suite
```

License
-------

MIT
