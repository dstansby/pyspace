from heliopy.data import util
from datetime import datetime


def test_montly_intervals():
    intervals = util.Downloader.intervals_monthly(
        datetime(1992, 11, 1), datetime(1992, 12, 1))
    assert len(intervals) == 2


def test_yearly_intervals():
    intervals = util.Downloader.intervals_yearly(
        datetime(1992, 11, 1), datetime(1993, 2, 1))
    assert len(intervals) == 2
