# AnomalyDetection and BreakoutDetection in python
This is a python implementation of Twitter's AnomalyDetection and BreakoutDetection.

## Install
The dependencies contain C++ and Fortran code, so that you need gcc installed.
Checkout the code, enter the folder and run:
```
pip install -r requirements.txt
```
When use this as a library, please include the line for "pyloess" from "requirements.txt" in your "requirements.txt".

## Usage
The parameters are the same as the AnomalyDetectionVec in Twitter's AnomalyDetection (except the plot related ones).
You need to put your time series data into a list of float numbers:
```
from anoms import detect_anoms
from breakout import detect_breakout

x = list()

\# put the data into x

res = detect_anoms(x, max_anoms=0.02, alpha=0.01, direction='both')
```
`res` will be a list of int numbers, consists the index of detected anomalies in `x`.
If `e_value=True` is set, `res` will be a tuple, 
whose first value is the list of index of detected anomalies 
and the second value is the list of expected values.
```
res = detect_breakout(x, min_size=24, method='multi', beta=0.001, degree=1)
```
`res` will be a list of int numbers, consists the index of detected breakout in `x`.
