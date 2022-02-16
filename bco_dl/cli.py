#!/usr/bin/env python
# coding: utf-8
"""
Simply ftpretty based interface to download data from Barbados Cloud
Observatory FTP server

- overview: https://barbados.mpimet.mpg.de/
- available data:
  http://bcoweb.mpimet.mpg.de/systems/data_availability/DeviceAvailability.html
"""
import bz2
import datetime
from pathlib import Path

import netCDF4
import xarray as xr

from .remote_paths import get_remote_path_format

HOSTNAME = "ftp-projects.zmaw.de"


def gen_queries(p_format, t_start, t_end):
    """
    For a path format which includes datetime placeholders generate the queries
    which will fetch all files in the time range between `t_start` and `t_end`
    """
    if "%d" in p_format:
        n_days = (t_end - t_start).days
        for n in range(n_days):
            t = t_start + datetime.timedelta(days=n)
            # TODO: could improve this by jumping in months/years at a time
            yield datetime.datetime.strftime(t, p_format)
    elif "%m" in p_format:
        n_days = (t_end - t_start).days
        m = t_start.month
        for n in range(n_days):
            t = t_start + datetime.timedelta(days=n)
            if t.month != m and t.month != m % 12:
                m += 1
                yield datetime.datetime.strftime(t, p_format)
    else:
        raise NotImplementedError


def get_dataset(c_ftp, remote_path, in_memory=False, local_root_path="."):
    """
    Fetch and load a dataset at path `remote_path` using ftpretty client
    `c_ftp`. Optionally load files in memory instead of writing a local file.
    """
    p = remote_path
    p_local = Path(local_root_path) / remote_path
    if in_memory:
        ds_bytes = c_ftp.get(p)
        if p.name.endswith(".bz2"):
            ds_bytes = bz2.decompress(ds_bytes)
        nc4_ds = netCDF4.Dataset("__in_memory_dataset__", memory=ds_bytes)
        store = xr.backends.NetCDF4DataStore(nc4_ds)
        return xr.open_dataset(store)
    else:
        if not p_local.exists():
            p_local.parent.mkdir(parents=True, exist_ok=True)
            c_ftp.get(p, p_local)
        return xr.open_dataset(p_local, chunks=dict(time=10))


def get_datasets_in_time_range(
    c_ftp,
    product,
    t_start,
    t_end,
    in_memory=False,
    product_kws={},
    debug=False,
    local_root_path=".",
    query_only=False,
):
    """
    Using `c_ftp` ftpretty client instance download all datasets available for
    `product` between `t_start` and `t_end`. Extra keyword args (version, band
    name, etc) can be provided through `product_kws`
    """
    product_path_format = get_remote_path_format(product, **product_kws)
    remote_paths = []
    for qr in gen_queries(product_path_format, t_start, t_end):
        if debug:
            print("query", qr)
        remote_paths += c_ftp.list(qr)
    ds_ = []
    if query_only:
        return remote_paths

    for remote_path in remote_paths:
        if debug:
            print("download", remote_path)
        ds = get_dataset(
            c_ftp, remote_path, in_memory=in_memory, local_root_path=local_root_path
        )
        ds_.append(ds)
    if len(ds_) > 0:
        return xr.concat(ds_, dim="time")
    else:
        raise Exception("No data found")
