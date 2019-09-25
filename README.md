# BCO FTP download utility

Install with pip (without source directory):

```bash
$> pip install .
```

# Usage

See [notebook](notebooks/usage.ipynb) for example usage.

```python
import ftpretty
import datetime

import bco_dl

c = ftpretty.ftpretty(bco_dl.HOSTNAME, user, passwd)

t_start = datetime.datetime(2018, 12, 29)
t_end = datetime.datetime(2019, 1, 2)
ds_velocity = bco_dl.get_datasets_in_time_range(c, 'vertical_velocity', t_start, t_end)
ds_radar = bco_dl.get_datasets_in_time_range(c, 'radar', t_start, t_end)
```
