#signal detection
import numpy as np
import scipy.stats as spi

class SignalDetection:
    def __init__(self, hits, misses, falseAlarms, correctRejections):
        self.hits = hits
        self.misses = misses
        self.falseAlarms = falseAlarms
        self.correctRejections = correctRejections

    def hitRate(self):
        return self.hits / (self.hits + self.misses)
    
    def falseAlarmRate(self):
        return self.falseAlarms / (self.falseAlarms + self.correctRejections)
    
    def d_prime(self):
        return spi.norm.ppf(self.hitRate()) - spi.norm.ppf(self.falseAlarmRate())

    def criterion(self):
        return -0.5 * (spi.norm.ppf(self.hitRate()) + spi.norm.ppf(self.falseAlarmRate()))