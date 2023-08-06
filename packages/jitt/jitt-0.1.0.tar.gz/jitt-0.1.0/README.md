# jitt
simple jitter tool

Takes a baseline delay value, a percentage to calculate the min/max for allowed jitter values, and a desired precision; returns a float.

### Installation
```
pip install jitt
python3 -m pip install jitt
```

### Usage
```
from jitt import Jitt
j = Jitt(delay=10.5, percent=25, precision=3).jitter
print(j)

# misc results for above values (min: 7.875 / max: 13.125)
# 8.177
# 12.975
# 10.565
# 9.022
# 11.43 (trailing zero is truncated)
```