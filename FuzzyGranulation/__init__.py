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

import logging
from time import time

import numpy as np
from matplotlib import pyplot

from StrongFuzzyPartition import StrongFuzzyPartition

np.seterr(divide='ignore', invalid='ignore')


class FuzzyGranulation(object):
    '''
    This class occupies to perform the fuzzy granulation using a defined Strong
    Fuzzy Partition (SFP).
    '''

    def __init__(self, dataset, centroids, labels):
        '''
        Initializes the instances of the class.
        
        :Parameters:
        dataset: the list of elements.
        centroids: the list of clusters centroids.
        
        '''
        self._dataset = dataset
        self._labels = labels
        self._sfp = StrongFuzzyPartition(centroids, labels, (min(self._dataset), max(self._dataset)))
        self._table = None

    def __call__(self):
        '''
        This function creates the table of membership degree to all fuzzy sets
        of Strong Fuzzy Partition for all dataset elements.
          
        :Returns:
        self.table: list formed by every item of the dataset and its membership
                    degree to at least 2 fuzzy sets.
        
        '''
        logging.warning("\nFuzzy Granulation process in execution...")
        t0 = time()
        self._table = [(x, self._sfp.membership(x)) for x in self._dataset]
        tf = time()
        logging.warning(
            "Time elapsed in granulation process: {0:.3f} seconds.".format(tf - t0))
        return self._table

    def plot(self, xlabel, ylabel, path, title, eps=10):
        '''
        This function draws the granulated elements of the dataset.
        
        :Parameters:
        xlabel: the label for x axis.
        ylabel: the label for y axis.
        
        '''
        pyplot.close('all')
        points = {label: [] for label in self._labels}
        for price, memberships in self._table:
            for label, ms in memberships:
                # if ms > 0:
                points.get(label).append((price, ms))
        minY, maxY = (0.0, 1.0)
        minU, maxU = (min(self._dataset), max(self._dataset))
        _, ax = pyplot.subplots()
        for _, fs in self._sfp():
            x, y = zip(*fs._points)
            ax.plot(x, y, color="k", linestyle=":")
        for label, pts in points.items():
            x, y = zip(*pts)
            ax.plot(x, y, marker="o", linestyle="", label=label)
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), numpoints=1)
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_xlim(minU - eps, maxU + eps)
        ax.set_ylim(minY, maxY + 0.2)
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        pyplot.savefig(path + 'Granules.png', bbox_inches='tight')

    def plotSFP(self, xlabel, ylabel, path, str="GranulesSFP"):
        '''
        This function calls the StrongFuzzyPartition method plot() in order
        to draw the fuzzy sets.
        
        :Parameters:
        xlabel: label for x axis.
        ylabel: label for y axis.
        
        '''
        self._sfp.plot(xlabel, ylabel, path, str)
