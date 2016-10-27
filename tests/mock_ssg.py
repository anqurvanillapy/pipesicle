from metassg import MetaSSG


class MockPageGenerator(MetaSSG):
    """\
    Mock simple SSG for single file input/output, e.g. slideshow generator
    """
    def __init__(self):
        super().__init__('foo', 'bar')

    def render(self):
        pass


class MockSiteGenerator(MetaSSG):
    """\
    Mock SSG for multiple file-input/output in directory, e.g. blog, wiki
    """
    def __init__(self):
        super().__init__('foo', 'bar')

    def render(self):
        pass
        
