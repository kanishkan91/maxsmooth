import numpy as np
from scipy.special import legendre


class Models_class(object):
    def __init__(self, params, x, y, N, mid_point, model_type, model, args):
        self.x = x
        self.y = y
        self.N = N
        self.params = params
        self.mid_point = mid_point
        self.model_type = model_type
        self.model = model
        self.args = args
        self.y_sum = self.fit()

    def fit(self):

        if self.model is None:
            if self.model_type == 'normalised_polynomial':

                y_sum = self.y[self.mid_point]*np.sum([
                    self.params[i]*(self.x/self.x[self.mid_point])**i
                    for i in range(self.N)], axis=0)

            if self.model_type == 'polynomial':

                y_sum = np.sum(
                    [self.params[i]*(self.x)**i for i in range(self.N)],
                    axis=0)

            if self.model_type == 'log_MSF_polynomial':

                y_sum = np.sum(
                    [self.params[i]*np.log10(self.x/self.x[self.mid_point])**i for i in range(self.N)],
                    axis=0)

            if self.model_type == 'MSF_2017_polynomial':

                y_sum = np.sum([
                    self.params[i]*(self.x-self.x[self.mid_point])**i
                    for i in range(self.N)], axis=0)

            if self.model_type == 'legendre':
                interval = np.linspace(-0.999, 0.999, len(self.x))
                lps = []
                for l in range(self.N):
                    P = legendre(l)
                    lps.append(P(interval))
                lps=np.array(lps)
                """print(lps)
                print(self.params)"""
                y_sum = np.sum([self.params[i]*lps[i] for i in range(self.N)], axis=0)
                """print(y_sum.shape)
                import pylab as pl
                pl.plot(self.x, y_sum)
                pl.plot(self.x, self.y)
                pl.show()"""
        if self.model is not None:
            if self.args is None:
                y_sum = self.model(
                    self.x, self.y, self.mid_point, self.N, self.params)
            if self.args is not None:
                y_sum = self.model(
                    self.x, self.y, self.mid_point, self.N, self.params,
                    *self.args)
        return y_sum