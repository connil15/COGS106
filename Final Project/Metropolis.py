import numpy as np

class Metropolis:
    def __init__(self, logTarget, initialState):
        self.logTarget = logTarget
        self.initialState = initialState
        self.samples = []
        self.stepSize = 1

    def __accept(self, proposal):
        diff = self.logTarget(proposal) - self.logTarget(self.initialState)
        acceptanceProb = min(1, np.exp(diff))
        return np.random.rand() < acceptanceProb

    def adapt(self, blockLengths):
        acceptanceRates = []
        for blockLength in blockLengths:
            accepted = 0
            for i in range(blockLength):
                proposal = np.random.normal(self.initialState, self.stepSize)
                if self.__accept(proposal):
                    self.initialState = proposal
                    accepted += 1
                acceptanceRates.append(accepted / blockLength)
            meanAcceptanceRate = np.mean(acceptanceRates)
            self.stepSize *= np.exp((meanAcceptanceRate - 0.4) / 10)
        return self

    def sample(self, nSamples):
        for i in range(nSamples):
            proposal = np.random.normal(self.initialState, self.stepSize)
            if self.__accept(proposal):
                self.initialState = proposal
            self.samples.append(self.initialState)
        return self
    
    def summary(self):
        mean = np.mean(self.samples)
        interval = np.percentile(self.samples, [2.5, 97.5])
        return {'mean': mean, 'c025': interval[0], 'c975': interval[1]}