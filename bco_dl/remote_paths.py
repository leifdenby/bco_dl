"""
Definitions of paths for BCO datasets
"""
from pathlib import Path


def cloudbase():
    return "A_Cloud_base_heights/CEILO__*__%Y%m.nc"


def vertical_velocity(instrument="WBAND_LIDAR"):
    """
    available instruments: TESTBAND_LIDAR (until 10/2019)
                           WBAND_LIDAR (from 02/2019)
    """
    return (
        "L_Vertical_velocity/{instrument}/%Y%m/"
        "WindLidar__Deebles_Point*__%Y%m%d.nc*"
        "".format(instrument=instrument)
    )


def radar(band="Ka", freq="2s", instrument="MBR2"):
    return (
        f"B_Reflectivity/{band}-Band/{instrument}/{freq}/%Y%m/"
        f"MMCR__MBR2__Spectral_Moments__{freq}__155m-18km__%y%m%d.nc"
    )


def lidar(instrument="CORAL", resolution="high"):
    """
    Instruments currently on BCO ftp: CORAL, EARLI, LICHT
    """
    if instrument == "CORAL":
        subpath = f"nc/{resolution}Resolution"
    else:
        subpath = "nc"

    path = Path(
        f"R_RamanLidar/RamanLidar-{instrument}/3_QuickLook/{subpath}/ql%y%m/ql%y%m%d"
    )

    if instrument == "CORAL":
        # coral_hr_200109_0000_0100_b.nc
        fn_pattern = "coral_hr_%y%m%d_????_????_?.*"
    else:
        fn_pattern = "ql%y%m%d0000.*"
    return str(path / fn_pattern)


def meteorology():
    return "I_Meteorology_2m/%Y%m/" "Meteorology__Deebles_Point__2m_10s__%Y%m%d.nc"


def liquid_water_content(location="BCO"):
    """
    Rainrates derived from the MRR at BCO or CIMH
    """
    if location not in ["BCO", "CIMH"]:
        raise FileNotFoundError(f"No data for location `{location}`")

    return (
        f"H_Liquid_water_content/{location}/%Y%m/"
        "MRR__Deebles_Point__LWC__60s_100m__%Y%m%d.nc"
    )


def get_remote_path_format(product, **kwargs):
    if product not in globals():
        raise NotImplementedError(
            "Please add a remote path definition to "
            "{} for {}".format(__file__, product)
        )
    else:
        return globals()[product](**kwargs)
