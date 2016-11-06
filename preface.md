title:  Postocol

**Posting Protocol**, SSG (static site generator) abstract class for extensible
use.

> Fork me on [GitHub](https://github.com/anqurvanillapy/postocol)!

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
