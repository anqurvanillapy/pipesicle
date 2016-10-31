postocol
========

**Posting Protocol**, SSG (Static site generator) abstract class for extensible
use. Only supported Python 3.5+, for the compatibility of 3.4, 2.7 or other
versions not tested and guaranteed.

Requirements
------------

- [Jinja2](http://jinja.pocoo.org/) `>=2.8`

Installation
------------

Not on PyPI yet. Please clone and manually run the setup script.

```bash
$ git clone git@github.com:anqurvanillapy/postocol.git
$ cd postocol
$ python3 setup.py install # or use `-r` to specify requirements
```

API Reference
-------------

### Properties

#### `ifpath`

|Type|Default|
|:-:|:-:|
|`str`|`'content'`|

Input file/directory.

#### `tmplpath`

|Type|Default|
|:-:|:-:|
|`str`|`'templates'`|

Template directory, mainly used by `jinja2.Environment` with the loader
`jinja2.FileSystemLoader` for better flexibility.

#### `ofpath`

|Type|Default|
|:-:|:-:|
|`str`|`'site'`|

Output file/directory.

#### `staticpath`

|Type|Default|
|:-:|:-:|
|`str`|`'static'`|

Static assets directory.

#### `pymd_exts`

|Type|Default|
|:-:|:-:|
|`list`|`['meta']`|

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

### `Postocol.load_templates(fpath)`

|`fpath` Type|Return Type|
|:-:|:-:|
|`str`|`dict`|

Load all [valid templates](#workflow) from `fpath`, and return a dict with the
valid template types as keys, and the Jinja2 template paths as values.
**Attention, the template file extension should only be `.html`.**

### `Postocol.load_posts(fpath)`

|`fpath` Type|Return Type|
|:-:|:-:|
|`str`|`list`|

Load all valid Markdown posts from `fpath`, and return a list of their paths.
These extensions are only readable for this method: `.markdown`, `.mdown`,
`.mkdn`, `.md`, `.mkd`, `.mdwn`, `.mdtxt`, `.mdtext`, `.text` and `.txt`.

### `Postocol.render(posts)` (**abstract**)

|`posts` Type|Return Type|
|:-:|:-:|
|`list`|`list`|

Abstract method for rendering the loaded Markdown posts. You can use
[bs4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) and
[lxml](http://lxml.de/) to implement the rendering, but **most importantly,
returned list of pages (a page is a dict) should have 3 keys,** and they are
`content` (Markdown-generated stuff), `meta` (metadata of a post) and `fname`
(outpuf filename).

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
|`list`|`list`|Void|

Render the templates `tmpls` with the generated HTML `pages`, and write them
to `ofpath`. If `ofpath` is a file, the `fname` value in a page dict will be
overriden, and the method brings out the file `ofpath`.

Implementation Workflow
-----------------------

- There are **3** document types that Postocol mainly serves, which are:
    + Slideshow
    + Blog
    + Wiki
- Therefore, Postocol will by default trace **6** types of templates as follows:
    + `index`, for blog or wiki, or even the slideshow (because it can be stored
    in one static HTML file, hence assuming that it is an index page)
    + `post`, for blog or wiki, e.g. an article
    + `states`, mainly for wiki, a list containing the current states of a post,
    e.g. *unfinished*, *not proofread*, *stub*, etc., similarly the metadata
    + `properties`, for wiki or blog, a list of the properties of a post, e.g.
    *howto*, *daily*, *compsci*, *PoC*, etc., similarly the categories or tags
    + `misc`, something you want to provide independently, instead of listing in
    `index`, `states` or `properties`, e.g. *about*, *contact*, *resume*, etc.
    + `layout`, serving something above
- **Additionally**, `index`, `states` and `properties` could be automatically
generated from self-implemented `Postocol.render()` method.

### For slideshow generator

There is no need to `clean()` anything and `send_static()` for a slideshow
generator, so the workflow is simple:

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
(bar.md) --+     clean()   load_templates()   publish()  send_static()
           |        |           |                |             |
           v        v           v                v             v
       (content/) --+----- templates ---+--> (site/) --+-> (site/static/)
                    |                   |              +-- (index.html)
                    +-- posts -> pages -+              +-- (states.html)
                         ^         ^                   +-- (properties.html)
                         |         |                   +-- (foo.html)
                  load_posts()  render()               +-- (bar.html)
```

Example
-------

```python
from postocol import Postocol

import codecs
from os.path import basename, splitext
from markdown import Markdown
from bs4 import BeautifulSoup


class SSG(Postocol):
    """SSG Example"""
    tmplpath = 'templates'
    ifpath = 'content'

    def __init__(self):
        """Control flow goes here"""
        pass

    def render(self, posts):
        """Render pages"""
        pages = []

        for p in posts:
            with codecs.open(p, 'r', encoding='utf-8') as f:
                md = Markdown(extensions=self.pymd_exts)
                html = BeautifulSoup(md.convert(f.read()), 'lxml')
                html.html.hidden = True
                html.body.hidden = True # remove html and body tags
                meta = md.Meta
                fname = lambda x: '{}.html'.format(splitext(basename(x))[0])
                pages.append({'content': html,
                              'meta': meta,
                              'fname': fname(p)})

        return pages
```

Test
----

**Postocol** doesn't use any third-party testing libraries, for the built-in
`unittest` is decent for testing its basic functionality, which is able to be
used from the command line.

```bash
$ python3 -m unittest # use `-v` to show verbose of the test suite
```

License
-------

MIT
