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

from random import uniform
from time import time

import logging
import numpy as np
from numpy import array

from .FuzzyCMeans import FuzzyCMeans

np.seterr(divide='ignore', invalid='ignore')


class FuzzyClustering(object):
    """
    This class perform the fuzzy clustering of the data.
    """

    def __init__(self, trainingset, clusters=2):
        """
        Initializes the instance of the class.
        
        :Parameters:
        trainingset: the matrix of data to be classified;
        clusters: number of clusters required.
        
        """
        self._clusters = clusters
        self._trainingSet = array(trainingset)
        self._partitionMatrix = self._createRandomPartitionMatrix()

    def __call__(self, maxError=1.e-4, maxIter=100):
        """
        This function compute the clustering process.
        
        :Parameters:
        maxError: maximum error admitted;
        maxIter: maximum number of iterations admitted.
        
        :Returns:
        centroids: list of centers of clustered regions.
        
        """
        clustering = FuzzyCMeans(self._trainingSet, self._partitionMatrix)
        logging.warning("\nClustering process in execution...")
        logging.warning("Tollerance:" + str(maxError) + "- Maximum number of iterations:" + str(maxIter))
        t0 = time()
        centroids = clustering(emax=maxError, imax=maxIter)
        tf = time()
        logging.warning("Time elapsed in clustering process: {0:.3f} seconds.".format(tf - t0))
        return centroids.tolist()

    def _createRandomPartitionMatrix(self):
        """
        This function creates the partition matrix with random data.
        
        :Returns:
        the list that represents the partition matrix of random data.
        
        """
        U = []
        for _ in range(len(self._trainingSet)):
            cake = 1.0
            partition = []
            for _ in range(self._clusters - 1):
                cakeSlice = uniform(0, cake)
                partition.append(cakeSlice)
                cake -= cakeSlice
            partition.append(1 - sum(partition))
            U.append(partition)
        return array(U)
