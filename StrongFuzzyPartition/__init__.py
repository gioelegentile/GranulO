"""
	Copyright 2016 Gioele Gentile, Matteo Caliandro, Rocco Lillo, Rocco Maiullari
		
	This file is part of GranulO.

	GranulO is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	GranulO is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with GranulO.  If not, see <http://www.gnu.org/licenses/>.
"""

from matplotlib import pyplot

from Fuzzython.fsets.trapezoid import Trapezoid
from Fuzzython.fsets.triangular import Triangular


class StrongFuzzyPartition(object):
    '''
    This class occupies to define an uniform Strong Fuzzy Partition (SFP), a
    collection of triangular or trapezoidal fuzzy sets, where for each item of
    the data domain, the sum of the membership of all fuzzy sets is always 1.
    '''

    def __init__(self, prototypes, labels, interval):
        '''
        Initializes the instances of the class.
        If the parameter prototypes and labels have not the same number of
        items, an exception will be raised.
        
        
        :Parameters:
        prototypes: the list of prototypes.
        labels: list of labels associated to centroids.
        interval: pair formed by endpoints of the domain.
        
        '''
        self._prototypes = prototypes
        self._labels = labels
        self._inf, self._sup = interval
        self._N = len(self._prototypes)
        if self._N != len(self._labels):
            raise Exception(
                "[StrongFuzzyPartition constructor] Parameters \"prototypes\" (list) and \"labels\" (list) must have the same number of elements.")
        self._sfp = self.create()

    def __call__(self):
        '''
        This function returns the Strong Fuzzy Partition (self.sfp).
        
        '''
        return self._sfp

    def create(self, eps=1e-3):
        '''
        This function creates the Strong Fuzzy Partition using N fuzzy sets.
        
        :Returns:
        self.sfp: list of pairs where elements of each pair are the label and
                  the fuzzy set.
        
        '''
        f_0 = [Trapezoid((self._inf - eps, 1), (self._inf, 1), (self._prototypes[0], 1), (self._prototypes[1], 0))]
        f_i = [Triangular((self._prototypes[i - 1], 0), (self._prototypes[i], 1), (self._prototypes[i + 1], 0)) for i in
               range(1, self._N - 1)]
        f_n = [Trapezoid((self._prototypes[self._N - 2], 0), (self._prototypes[self._N - 1], 1), (self._sup, 1),
                         (self._sup + eps, 1))]
        partition = f_0 + f_i + f_n
        self._sfp = list(zip(self._labels, partition))
        return self._sfp

    def membership(self, x):
        '''
        This function calculates, for an element x of the dataset, the member-
        ship degree to each fuzzy set defined in the Strong Fuzzy Partition.
        
        :Parameters:
        x: item of the dataset.
        
        :Returns:
        list of pairs where elements of each pair are the label of fuzzy set
        and the membership degree of x to the fuzzy set.
        '''
        return [(label, float(mf(x))) for label, mf in self._sfp]

    def plot(self, xlabel, ylabel, path, str, eps=1e-3):
        '''
        This function draws fuzzy sets which define the Strong Fuzzy Partition.
        
        :Parameters:
        xlabel: the label for x axis.
        ylabel: the label for y axis.
        
        '''
        pyplot.close('all')
        minY, maxY = (0.0, 1.0)
        _, ax = pyplot.subplots()
        for center, (label, fs) in zip(self._prototypes, self._sfp):
            x, y = zip(*fs._points)
            ax.plot(x, y, color="k", linestyle="-", linewidth="1.5")
            ax.fill_between(x, y, color="#efefef")
            ax.plot([center, center], [minY, maxY], color="k", linestyle="--")
            ax.annotate(label, xy=(center, 1), xytext=(-3 * len(label), 5), textcoords="offset points")
        ax.set_title("Strong Fuzzy Partition that represents the granules of information\n")
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_xlim(self._inf - eps, self._sup + eps)
        ax.set_ylim(minY, maxY + 0.2)
        pyplot.savefig(path + str + '.png', bbox_inches='tight')
