"""
Definitions of paths for BCO datasets
"""

def cloudbase():
    return "A_Cloud_base_heights/CEILO__*__%Y%m.nc"

def vertical_velocity(version='1.01'):
    return ("L_Vertical_velocity/Version{version}/"
            "WindLidar__Deebles_Point*__%Y%m%d.nc*".format(version=version))

def radar(band='Ka', freq='2s'):
    return ("B_Reflectivity/{band}-Band/{freq}/%Y%m/"
            "MMCR__MBR__Spectral_Moments__{freq}__155m-18km__%y%m%d.nc"
            "".format(band=band, freq=freq))


def get_remote_path_format(product, **kwargs):
    if not product in globals():
        raise NotImplementedError('Please add a remote path definition to '
                                  '{} for {}'.format(__file__, product))
    else:
        return globals()[product](**kwargs)
