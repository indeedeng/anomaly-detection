# AnomalyDetection in python
This is a python implementation of Twitter's AnomalyDetection.

## Usage
The dependencies contain C++ and Fortran code, so that you need gcc installed.
The parameters are the same as the AnomalyDetectionVec in Twitter's AnomalyDetection (except the plot related ones).
You need to put your time series data into a list of float numbers:
```
from anoms import detect_anoms

x = list()

\# put the data into x

res = detect_anoms(x, max_anoms=0.02, alpha=0.01, direction='both')
```
`res` will be a list of int numbers, consists the index of detected anomalies in `x`.
If `e_value=True` is set, `res` will be a tuple, 
whose first value is the list of index of detected anomalies 
and the second value is the list of expected values.
