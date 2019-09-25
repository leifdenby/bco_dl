
def clip_datasets(dss, dim='time'):
    vmin, vmax = None, None
    for ds in dss:
        if vmin is None or ds[dim].min() > vmin:
            vmin = ds[dim].min()
        if vmax is None or ds[dim].max() < vmax:
            vmax = ds[dim].max()
    dss_clipped = []
    for ds in dss:
        dss_clipped.append(ds.sel(time=slice(vmin, vmax)))
    return dss_clipped
