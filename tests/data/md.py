# -*- coding: utf-8 -*-


markdown_text = {
    'fname': ['foo.md', 'bar.md'],
    'content': ["""\
title:      Hello
type:       post
states:     unfinished
properties: randumb
date:       January 1, 2001

# Foo

> bar

baz
""",
"""\
title:      Aloha
type:       index

# Hello, world!
"""]}


invalid_markdown_text = """\
title:      Qux

# Qux

This post got no types, invalid to be loaded.
"""
