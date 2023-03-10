import numpy as np
import unittest
import matplotlib.pyplot as plt

from SignalDetection import SignalDetection

#parameters
dPrime       = 1.5
criteriaList = [-0.5, 0, 0.5]
signalCount  = 1000
noiseCount   = 1000
sdtList      = SignalDetection.simulate(dPrime, criteriaList, signalCount, noiseCount)

#SignalDetection.plot_roc(sdtList)
SignalDetection.fit_roc(sdtList)
