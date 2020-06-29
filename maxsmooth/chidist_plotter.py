import numpy as np
import os
from itertools import product
import matplotlib.pyplot as plt

class chi_plotter(object):
    def __init__(self, N, **kwargs):

        self.N = N
        if self.N%1!=0:
            raise ValueError('N must be an integer or whole number float.')


        for keys, values in kwargs.items():
            if keys not in set(['chi','base_dir',
                'ifp_list', 'constraints',
                'fit_type', 'chi_squared_limit', 'cap', 'plot_limits']):
                raise KeyError("Unexpected keyword argument in parameter plotter.")

        self.base_dir = kwargs.pop('base_dir', 'Fitted_Output/')
        if type(self.base_dir) is not str:
            raise KeyError("'base_dir' must be a string ending in '/'.")
        elif self.base_dir.endswith('/') is False:
            raise KeyError("'base_dir' must end in '/'.")

        if not os.path.exists(self.base_dir):
            raise Exception("'base_dir' must exist and contain the outputted"
                + " evaluations and sign combinations from a maxsmooth fit."
                + " These can be obtained by running maxsmooth with"
                + " 'data_save=True'.")
        else:
            if not os.path.exists(self.base_dir + 'Output_Evaluation/'):
                raise Exception("No 'Output_Evaluation/' directory found in"
                    + " 'base_dir'.")
            if not os.path.exists(self.base_dir + 'Output_Signs/'):
                raise Exception("No 'Output_Signs/' directory found in"
                    + " 'base_dir'.")

        self.chi = kwargs.pop('chi', None)

        self.constraints = kwargs.pop('constraints', 2)
        if type(self.constraints) is not int:
            raise TypeError("'constraints' is not an integer")
        if self.constraints > self.N-1:
            raise ValueError("'constraints' exceeds the number of derivatives.")

        self.ifp_list = kwargs.pop('ifp_list', None)
        if self.ifp_list is not None:
            for i in range(len(self.ifp_list)):
                if type(self.ifp_list[i]) is not int:
                    raise TypeError("Entries in 'ifp_list' are not integer.")
                if self.ifp_list[i] < self.constraints:
                    raise ValueError('One or more specified derivatives for' +
                        ' inflection points is less than the minimum constrained' +
                        ' derivative.\n ifp_list = ' + str(self.ifp_list) + '\n' +
                        ' Minimum Constrained Derivative = ' + str(self.constraints))

        self.fit_type = kwargs.pop('fit_type', 'qp-sign_flipping')
        if self.fit_type not in set(['qp', 'qp-sign_flipping']):
            raise KeyError("Invalid 'fit_type'. Valid entries include 'qp'\n" +
                "'qp-sign_flipping'")

        self.chi_squared_limit = kwargs.pop('chi_squared_limit', None)
        self.cap = kwargs.pop('cap', None)
        if self.chi_squared_limit is not None:
            if isinstance(self.chi_squared_limit, int) or \
                isinstance(self.chi_squared_limit, float):
                pass
            else:
                raise TypeError("Limit on maximum allowed increase in chi squared" +
                    ", 'chi_squared_limit', is not an integer or float.")
        if self.cap is not None:
            if type(self.cap) is not int:
                    raise TypeError("The cap on directional exploration" +
                        ", 'cap', is not an integer.")

        self.plot_limits = kwargs.pop('plot_limits', False)

        self.plot()

    def plot(self):

        def signs_array(nums):
            return np.array(list(product(*((x, -x) for x in nums))))

        if self.ifp_list is not None:
            possible_signs = signs_array([1]*(self.N-self.constraints-len(self.ifp_list)))
        else:
            possible_signs = signs_array([1]*(self.N-self.constraints))

        plt.figure()
        j = np.arange(0, len(possible_signs),1)
        if self.chi is None:
            chi = np.loadtxt(self.base_dir + 'Output_Evaluation/'
                + str(self.N) +'_' + str(self.fit_type) + '.txt')
            signs = np.loadtxt(self.base_dir + 'Output_Signs/'
                + str(self.N) +'_' + str(self.fit_type) + '.txt')
            if len(signs) != len(possible_signs):
                index = []
                for p in range(len(signs)):
                    for i in range(len(possible_signs)):
                        if np.all(signs[p] == possible_signs[i]):
                            index.append(i)
                index, chi = zip(*sorted(zip(index, chi)))
                plt.plot(index, chi, ls='-')
            else:
                plt.plot(j, chi, marker='.', ls='-')
        else:
            chi = self.chi
            signs = np.loadtxt(self.base_dir + 'Output_Signs/'
                + str(self.N) +'_' + str(self.fit_type) + '.txt')
            if len(signs) != len(possible_signs):
                index = []
                for p in range(len(signs)):
                    for i in range(len(possible_signs)):
                        if np.all(signs[p] == possible_signs[i]):
                            index.append(i)
                index, chi = zip(*sorted(zip(index, chi)))
                plt.plot(index, chi, marker='.', ls='-')
            else:
                plt.plot(j, chi, marker='.', ls='-')

        if self.cap is None:
            self.cap = (len(possible_signs)//self.N) + self.N
        if self.chi_squared_limit is None:
            self.chi_squared_limit = 2*min(chi)

        for i in range(len(chi)):
            if chi[i] == min(chi):
                plt.plot(i, chi[i], marker='*')
                if self.plot_limits is True:
                    plt.vlines(i + self.cap, min(chi), max(chi), ls='--', label='Cap On Exp.', color='k', alpha=0.5)
                    plt.vlines(i - self.cap,  min(chi), max(chi), ls='--', color='k', alpha=0.5)
        if self.plot_limits is True:
            plt.hlines(self.chi_squared_limit, 0, len(possible_signs), ls='-.', label=r'Max. Increase\n' + ' in $\chi^2$', color='k', alpha=0.5)
        plt.xlim([j[0], j[-1]])
        plt.grid()
        plt.yscale('log')
        plt.ylabel(r'$\chi^2$')
        plt.xlabel('Sign Combination')
        plt.tight_layout()
        plt.savefig(self.base_dir + 'chi_distribution.pdf')
        plt.close()