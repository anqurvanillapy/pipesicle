# -*- coding: utf-8 -*-

from abc import abstractmethod, ABCMeta


class MetaSSG(metaclass=ABCMeta):
    """SSG base class"""
    @abstractmethod
    def clean(self):
        """Clean all legacy generated pages"""
        pass

    def load_templates(self, fpath):
        """\
        - Load templates using Jinja2 Environment
            + `fpath` can be filename and directory
            + FileSystemLoader is specified
        """
        pass

    @abstractmethod
    def render(self, posts):
        """\
        - Render the posts
            + Using Jinja2 render the templates
            + Publish pages into the destination directory
        """
        pass

    def send_static(self):
        """Send static assets to destination directory"""
        pass
