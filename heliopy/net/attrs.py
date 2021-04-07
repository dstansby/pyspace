from sunpy.net.attr import SimpleAttr
from sunpy.net.attrs import Source, Time, Instrument, Level, Provider


__all__ = ['Probe',
           'DataRate',
           'Version',
           'Source',
           'Time',
           'Instrument',
           'Level',
           'Provider',
           'Dataset']

# Trick the docs into thinking these attrs are defined in here.
for _a in (Source, Time, Instrument, Level, Provider):
    _a.__module__ = __name__


class Dataset(SimpleAttr):
    """
    Dataset ID.
    """


class Probe(SimpleAttr):
    """
    Probe number or name.

    Used when missions have multiple spacecraft, e.g. MMS has 4 probes
    named 1 to 4.
    """


class DataRate(SimpleAttr):
    """
    Data rate.
    """


class Version(SimpleAttr):
    """
    Data version.
    """
