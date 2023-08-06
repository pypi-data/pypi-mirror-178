# Objective Rating Metric for non ambigious signals according to ISO/TS 18571

Python implementation of ISO/TS 18571
https://www.iso.org/standard/62937.html

*ISO/TS 18571:2014 provides validation metrics and rating procedures to be used to calculate the level of correlation between two non-ambiguous signals obtained from a physical test and a computational model, and is aimed at vehicle safety applications. The objective comparison of time-history signals of model and test is validated against various loading cases under different types of physical loads such as forces, moments, and accelerations. However, other applications might be possible too, but are not within the scope of ISO/TS 18571:2014.*

## Installation guide

After cloning this repository, run the following command in your command line

```
python setup.py install
```

This will install the package to your environment. You can then import the package by simply adding the following to the top of your script:

```python
import objective_rating_metrics
```

## Usage
```python
import numpy as np
from objective_rating_metrics.rating import ISO18571

time_ = np.arange(0, 0.150, 0.0001)
ref = np.vstack((time_ + 0.02, np.sin(time_ * 20))).T
comp = np.vstack((time_, np.sin(time_ * 20) * 1.3 + 0.00)).T

iso_rating = ISO18571(reference_curve=ref, comparison_curve=comp)
print(iso_rating.overall_rating())
```
```
>>> 0.713
```

## Reference and further reading

* [ISO/TS 18571 norm](https://www.iso.org/standard/62937.html)
