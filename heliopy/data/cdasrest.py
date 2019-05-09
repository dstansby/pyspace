"""
Helper methods for using the CDAS REST web services.

For more information see https://cdaweb.sci.gsfc.nasa.gov/WebServices/REST/
"""
from datetime import datetime, time, timedelta
from dateutil.relativedelta import relativedelta
import pathlib
import tempfile
import wget

import requests
import requests.exceptions

import heliopy.data.util as util

CDAS_BASEURL = 'https://cdaweb.gsfc.nasa.gov/WS/cdasr/1'
CDAS_HEADERS = {'Accept': 'application/json'}


def _docstring(identifier, letter, description):
    ds = r"""
    {description} data.

    See https://cdaweb.sci.gsfc.nasa.gov/misc/Notes{letter}.html#{identifier}
    for more information.

    Parameters
    ----------
    starttime : datetime
        Interval start time.
    endtime : datetime
        Interval end time.

    Returns
    -------
    data : :class:`~sunpy.timeseries.TimeSeries`
    """.format(identifier=identifier,
               letter=letter,
               description=description)
    return ds


def _daysplitinterval(starttime, endtime):
    """
    Splits an interval into a list of dates.

    Parameters
    ----------
    starttime : datetime
        Start date/time of interval
    endtime : datetime
        End date/time of interval

    Returns
    -------
    intervals : list of datetime.date
    """
    assert starttime < endtime, 'Start datetime must be before end datetime'
    out = []
    starttime_orig = starttime
    while starttime.date() <= endtime.date():
        out.append(starttime.date())
        starttime += timedelta(days=1)
    return out


def _process_cdas(starttime, endtime, identifier, dataset, base_dir,
                  units=None, badvalues=None, warn_missing_units=True,
                  splitfun=None):
    """
    Generic method for downloading cdas data.

    Paramters
    ---------
    splitfun : callable, optional
        Must take (starttime, endtime) as arguments and return a list of dates.
    """
    relative_dir = pathlib.Path(identifier)
    daylist = _daysplitinterval(starttime, endtime)
    if splitfun is None:
        daylist = _daysplitinterval(starttime, endtime)
    else:
        daylist = splitfun(starttime, endtime)
    dirs = []
    fnames = []
    dates = []
    extension = '.cdf'
    for date in daylist:
        dates.append(date)
        filename = '{}_{}_{}{:02}{:02}'.format(
            dataset, identifier, date.year, date.month, date.day)
        fnames.append(filename)
        this_relative_dir = relative_dir / str(date.year)
        dirs.append(this_relative_dir)

    def download_func(remote_base_url, local_base_dir,
                      directory, fname, remote_fname, extension, date):
        return get_data(identifier, date,
                        enddate=date + relativedelta(months=6))

    def processing_func(cdf):
        return util.cdf2df(cdf, index_key='Epoch',
                           badvalues=badvalues)

    return util.process(dirs, fnames, extension, base_dir, '',
                        download_func, processing_func, starttime,
                        endtime, units=units, download_info=dates,
                        warn_missing_units=warn_missing_units)


def get_variables(dataset, timeout=10):
    """
    Queries server for descriptions of variables in a dataset.

    Parameters
    ----------
    dataset : string
        Dataset identifier.
    timeout : float, optional
        Timeout on the CDAweb remote requests, in seconds. Defaults to 10s.

    Returns
    -------
    dict
        JSON response from the server.
    """
    dataview = 'sp_phys'
    url = '/'.join([
        CDAS_BASEURL,
        'dataviews', dataview,
        'datasets', dataset,
        'variables'
    ])
    response = requests.get(url, headers=CDAS_HEADERS, timeout=timeout)
    return response.json()


def get_cdas_url(startdate, vars, dataset, timeout=10, enddate=None):
    """
    Get URL to download CDAS data.

    Parameters
    ----------
    startdate : datetime.date
    vars :
    dataset :
    timeout : int, optional
    enddate : datetime.data, optional
        If ``None``, gets the URL for a single day of data.

    Returns
    -------
    url : str
    """
    if enddate is None:
        enddate = startdate
    starttime = datetime.combine(startdate, time.min)
    endtime = datetime.combine(enddate, time.max)
    dataview = 'sp_phys'
    if vars is None:
        try:
            var_info = get_variables(dataset, timeout=timeout)
        except requests.exceptions.ReadTimeout:
            raise util.NoDataError(
                'Connection to CDAweb timed out when downloading '
                f'{dataset} data for date {date}.')

        if not len(var_info):
            raise util.NoDataError(
                f'No {dataset} data available for date {date}')

        vars = [v['Name'] for v in var_info['VariableDescription']]

    uri = '/'.join(['dataviews', dataview,
                    'datasets', dataset,
                    'data',
                    ','.join([starttime.strftime('%Y%m%dT%H%M%SZ'),
                              endtime.strftime('%Y%m%dT%H%M%SZ')]),
                    ','.join(vars)
                    ])
    url = '/'.join([CDAS_BASEURL, uri])
    return url


def get_data(dataset, date, vars=None, verbose=True, timeout=10, enddate=None):
    """
    Download CDAS data.

    Parameters
    ----------
    dataset : string
        Dataset identifier.
    date : datetime.date
        Date to download data for.
    vars : list of str, optional
        Variables to download. If ``None``, all variables for the given
        dataset will be downloaded.
    verbose : bool, optional
        If ``True``, show a progress bar whilst downloading.
    timeout : float, optional
        Timeout on the CDAweb remote requests, in seconds. Defaults to 10s.
    enddate : datetime.data, optional
        If ``None``, gets a single day of data.

    Returns
    -------
    data_path : str
        Path to downloaded data (stored in a temporary directroy)
    """
    url = get_cdas_url(date, vars, dataset, timeout=timeout, enddate=enddate)
    params = {'format': 'cdf', 'cdfVersion': 3}
    response = requests.get(
        url, params=params, headers=CDAS_HEADERS, timeout=timeout)
    if 'FileDescription' in response.json():
        print('Downloading {} for date {}'.format(dataset, date))
        data_path = wget.download(
            response.json()['FileDescription'][0]['Name'],
            tempfile.gettempdir(),
            bar=wget.bar_adaptive if verbose else None
        )
        if verbose:
            print('')
    else:
        raise util.NoDataError(
            'No {} data available for date {}'.format(dataset, date))
    return data_path
