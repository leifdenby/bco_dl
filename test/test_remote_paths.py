import datetime
import inspect

import conftest
import ftpretty
import pytest

import bco_dl
from bco_dl import remote_paths


def _find_remote_path_names():
    function_names = [
        fn_name
        for (fn_name, fn) in inspect.getmembers(remote_paths, inspect.isfunction)
    ]
    function_names = [
        fn_name for fn_name in function_names if fn_name != "get_remote_path_format"
    ]
    return function_names


SOURCES = _find_remote_path_names()

QUERY_TIMES = dict(
    lidar=("2020-01-08T15:00", "2020-01-09T16:00"),
    radar=("2018-08-02T15:00", "2018-08-03T16:00"),
    vertical_velocity=("2019-08-02T15:00", "2019-08-03T16:00"),
)


@pytest.mark.parametrize("source_name", SOURCES)
def test_remote_path(source_name):
    c = ftpretty.ftpretty(bco_dl.HOSTNAME, conftest.username, conftest.password)

    if source_name in QUERY_TIMES:
        t_start, t_end = [
            datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M")
            for s in QUERY_TIMES[source_name]
        ]
    else:
        t_start = datetime.datetime(2018, 12, 29)
        t_end = datetime.datetime(2019, 1, 2)

    remote_paths = bco_dl.get_datasets_in_time_range(
        c, source_name, t_start, t_end, debug=True, query_only=True
    )
    assert len(remote_paths) > 0
