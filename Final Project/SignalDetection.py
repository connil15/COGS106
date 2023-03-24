import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import sklearn.metrics as metrics
import scipy as scipy

#Implement class based on signal detection theory
class SignalDetection:
    #Class constructor
    def __init__(self, hits, misses, falseAlarms, correctRejections):
        #signal detection theory variables
        self.hits = hits 
        self.misses = misses
        self.falseAlarms = falseAlarms
        self.correctRejections = correctRejections

    #class method to get the hit rate: hits/total signal trials
    def hit_rate(self):
        #Check for Corruption
        if(self.hits < 0 or self.misses < 0):
            raise ValueError("Hits or Misses cannot be negative!")
        return self.hits / (self.hits + self.misses)

    #class method to get the false alarm rate: false alarms/total noise trials
    def falseAlarm_rate(self):
        #Check for Corruption
        if(self.falseAlarms < 0 or self.correctRejections < 0):
            raise ValueError("False Alarms or Correct Rejections cannot be negative!")
        return self.falseAlarms / (self.falseAlarms + self.correctRejections)

    #class method to calculate d': Z(H) - Z(FA), Z = stats.norm.ppf
    def d_prime(self):
        #get z values
        z_hit = stats.norm.ppf(self.hit_rate()) 
        z_falseAlarm = stats.norm.ppf(self.falseAlarm_rate())
        #return d'
        return z_hit-z_falseAlarm

    #class method to get the criterion: -0.5*(Z(H) + Z(FA)), Z = stats.norm.ppf
    def criterion(self):
        #get Z values
        z_hit = stats.norm.ppf(self.hit_rate())
        z_falseAlarm = stats.norm.ppf(self.falseAlarm_rate())
        #return criterion
        return -0.5*(z_hit + z_falseAlarm)
    
    def __add__(self, other):
        return SignalDetection(self.hits + other.hits, self.misses + other.misses, self.falseAlarms + other.falseAlarms, self.correctRejections + other.correctRejections)

    def __mul__(self, scalar):
        return SignalDetection(self.hits * scalar, self.misses * scalar, self.falseAlarms * scalar, self.correctRejections * scalar)

    @staticmethod
    def simulate(dPrime, criteriaList, signalCount, noiseCount):
        sdtList = []
        for i in range(len(criteriaList)):
            #hit_rate & falseAlarm_rate
            z_hit = dPrime/2 + criteriaList[i]
            z_falseAlarm = - dPrime/2 + criteriaList[i]

            #hits & misses
            hits = np.random.binomial(signalCount, stats.norm.cdf(z_hit))
            misses = signalCount - hits

            #falseAlarm & correct rejection
            falseAlarms = np.random.binomial(noiseCount, stats.norm.cdf(z_falseAlarm))
            correctRejections = noiseCount - falseAlarms

            #make sdList
            sdtList.append(SignalDetection(hits, misses, falseAlarms, correctRejections))

        return sdtList
    
    @staticmethod    
    def plot_roc(sdtList):
        # create arrays to store x and y coordinates
        x_points = np.zeros(len(sdtList))
        y_points = np.zeros(len(sdtList))
        
        # loop over sdtList to calculate hit rate and false alarm rate
        for i, sdt in enumerate(sdtList):
            x_points[i] = sdt.falseAlarm_rate()
            y_points[i] = sdt.hit_rate()
        
        # plot
        plt.plot(x_points, y_points, 'o')
        plt.plot([0, 1], [0, 1], '--')
        plt.title('Receiver Operating Characteristic')
        plt.xlim([0, 1])
        plt.ylim([0, 1])
        plt.ylabel('Hit Rate')
        plt.xlabel('False Alarm Rate')
        #plt.show()

    def nLogLikelihood(self, hit_rate, falseAlarm_rate):
        ell = -self.hits * np.log(hit_rate) -self.misses * np.log(1-hit_rate) - self.falseAlarms * np.log(falseAlarm_rate) - self.correctRejections * np.log(1-falseAlarm_rate)
        return ell

    @staticmethod
    def rocCurve(falseAlarmRate, a):
        hitRate = []
        for i, falseAlarm in enumerate(falseAlarmRate):
            hitRate.append(stats.norm.cdf(a + stats.norm.ppf(falseAlarm)))
        return hitRate

    @staticmethod
    def rocLoss(a, sdtList):
        falseAlarmRate = []
        for i, sdt in enumerate(sdtList):
            falseAlarmRate.append(sdt.falseAlarm_rate())
        hitRate = sdt.rocCurve(falseAlarmRate, a)
        loss_sum = 0
        for i, sdt in enumerate(sdtList):
            loss = (np.sum(sdt.nLogLikelihood(hitRate[i], falseAlarmRate[i])))
            loss_sum += loss
        return loss_sum

    @staticmethod
    def fit_roc(sdtList):
        #single parameter
        def loss_func(a):
            loss_sum = 0
            for sdt in sdtList:
                loss_sum = sdt.rocLoss(a, sdtList)
            return loss_sum
        
        #a_hat
        a_rand = 0
        result = scipy.optimize.minimize(loss_func, a_rand)
        a_hat = result.x[0]

        #TPR/FPR
        falseAlarmRate = np.linspace(0, 1, num=100)
        for i, sdt in enumerate(sdtList):
            fitted_hits = sdt.rocCurve(falseAlarmRate, a_hat)

        #plot
        SignalDetection.plot_roc(sdtList)
        plt.plot(falseAlarmRate, fitted_hits, label='Fitted curve')
        plt.show()  

        return a_hat
 