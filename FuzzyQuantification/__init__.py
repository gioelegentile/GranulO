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

from matplotlib import pyplot

from StrongFuzzyPartition import StrongFuzzyPartition


class FuzzyQuantification(object):
    '''
    This class occupies to perform the fuzzy quantification using a SFP.
    '''

    def __init__(self, prototypes, qlabels, granules, glabels):
        '''
        Inizializes the instances of the class.
        
        :Parameters:
        prototypes: the list of prototypes.
        qlabels: the list of quantifiers labels.
        granules: the list of granules.
        glabels: the list of granules labels.
        
        '''
        self._granules = granules
        self._granuleslabels = glabels
        self._quantifiers = StrongFuzzyPartition(prototypes, qlabels, (0.0, 1.0))
        self.cardinalities = None
        self.quantification = None

    def __call__(self):
        '''
        This function maps for all fuzzy granule cardinality the relative
        membership degree to all fuzzy quantifiers. It returns a list of
        dictionaries; in all dictionaries are present all granules membership
        degrees to quantifiers fuzzy sets.
                
        '''
        logging.warning("\nFuzzy Quantification process in execution...")
        t0 = time()
        self.cardinalities = {granule: self.sigmaCount(granule) for granule in self._granuleslabels}
        self.quantification = {
            granule: {quant: float(fs(cardinality)) for quant, fs in self._quantifiers()}
            for granule, cardinality in self.cardinalities.items()}
        tf = time()
        logging.warning("Time elapsed in quantification process: {0:.3f} seconds.".format(tf - t0))
        return self.quantification

    def plotCardinalities(self, xlabel, ylabel, title, path):
        '''
        This function plots the cardinalities of the granules and the relative
        membership degree to fuzzy sets that represent the quantifiers.
        
        :Parameters:
        xlabel: the label for x axis.
        ylabel: the label for y axis.
        
        '''
        pyplot.close('all')
        minX, maxX = (0.0, 1.0)
        minY, maxY = minX, maxX
        _, ax = pyplot.subplots()
        for label, fs in self._quantifiers():
            x, y = zip(*fs._points)
            ax.plot(x, y, color="k", linestyle=":")
            ax.annotate(label, xy=(x[1], 1), xytext=(-3 * len(label), 5), textcoords="offset points")
        for granule, ms in self.quantification.items():
            y = [value for value in ms.values() if value > 0]
            x = [self.cardinalities.get(granule)] * len(y)
            ax.plot(x, y, marker="o", linestyle="", label=granule)
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), numpoints=1)
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_xlim(minX, maxX)
        ax.set_ylim(minY, maxY + 0.2)
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        pyplot.savefig(path + 'Cardinalities.png', bbox_inches='tight')

    def plotQuantifiers(self, xlabel, ylabel, path, str="CardinalitiesSFP"):
        '''
        This function calls the StrongFuzzyPartition method plot() in order
        to draw the fuzzy sets.
        
        :Parameters:
        xlabel: label for x axis.
        ylabel: label for y axis.
        
        '''
        self._quantifiers.plot(xlabel, ylabel, path, str)

    def sigmaCount(self, granule):
        '''
        This function calculates the sigma count measure that calculates the
        cardinality for a fuzzy granule.
        
        :Parameters:
        granule: the fuzzy granule. 
        
        :Returns:
        the value of calculated sigma-count.
        
        '''
        G = [element.get(granule) for element in self._granules]
        return sum(G) / len(self._granules)
