"""
Definitions of paths for BCO datasets
"""

def cloudbase():
    return "A_Cloud_base_heights/CEILO__*__%Y%m.nc"

def vertical_velocity(instrument="WBAND_LIDAR"):
    """
    available instruments: TESTBAND_LIDAR (until 10/2019)
                           WBAND_LIDAR (from 02/2019)
    """
    return ("L_Vertical_velocity/{instrument}/%Y%m/"
            "WindLidar__Deebles_Point*__%Y%m%d.nc*"
            "".format(instrument=instrument))

def radar(band='Ka', freq='2s'):
    return ("B_Reflectivity/{band}-Band/{freq}/%Y%m/"
            "MMCR__MBR__Spectral_Moments__{freq}__155m-18km__%y%m%d.nc"
            "".format(band=band, freq=freq))


def lidar(instrument='CORAL', resolution='high'):
    """
    Instruments currently on BCO ftp: CORAL, EARLI, LICHT
    """
    if instrument == "CORAL":
        subpath = "nc/{resolution}Resolution".format(resolution)
    else:
        subpath = "nc"

    return ("R_RamanLidar-{instrument}/3_QuickLook/{subpath}/ql%y%m/"
            "jl%y%m%d0000.*".format(instrument=instrument, subpath=subpath))


def meteorology():
    return ("I_Meteorology_2m/%Y%m/"
            "Meteorology__Deebles_Point__2m_10s__%Y%m%d.nc")

def get_remote_path_format(product, **kwargs):
    if not product in globals():
        raise NotImplementedError('Please add a remote path definition to '
                                  '{} for {}'.format(__file__, product))
    else:
        return globals()[product](**kwargs)
