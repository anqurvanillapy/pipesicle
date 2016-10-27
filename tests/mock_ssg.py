from metassg import MetaSSG


class MockSSG(MetaSSG):
    """\
    - Mock SSG for multiple usage, e.g.
        + slideshow generator (without `clean()` method)
        + blog, wiki (with `clean()` method)
    """
    def __init__(self):
        super().__init__('foo', 'bar')

    def render(self):
        pass
