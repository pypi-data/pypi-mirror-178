"""
this is the package sphinxcontrib.console.
"""
__version__ = (1, 2, 0)

from .excel import ExcelDirective

def setup(application):
    """
    setup extension.
    """
    application.add_directive('excel', ExcelDirective)
    return {"version": __version__, "parallel_read_safe": True}
