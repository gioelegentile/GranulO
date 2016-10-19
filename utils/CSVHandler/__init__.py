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

import csv


class CSVHandler(object):
    '''
    This class provides functions to read/write data from/to a csv file.
    '''

    def __init__(self, filename):
        '''
        Initializes the instance of the class.
        
        :Parameters:
        filename: name of csv file to open.
        
        '''
        self.filename = filename

    def read(self):
        '''
        This function reads from the csv and stores data in a matrix.
        
        :Returns:
        dataset: matrix of data stored in csv file.
        
        '''
        dataset = []
        try:
            with open(self.filename, "r") as csvfile:
                reader = csv.reader(csvfile, delimiter=",")
                dataset = [row for row in reader]
        except:
            raise
        return dataset

    def readDict(self):
        '''
        This function reads from the csv and stores data in an array.
        The csv rows will stored as different dictionaries within the array.
        
        :Returns:
        dataset: the list where each row is a dictionary that represents
                 the csv file row.
        dictkeys: the list of dictionaries keys.
        
        '''
        dataset = []
        try:
            with open(self.filename, "r") as csvfile:
                reader = csv.DictReader(csvfile)
                dataset = [row for row in reader]
            if dataset:
                with open(self.filename, "r") as header:
                    dictkeys = header.readline().replace("\n", "").split(",")
        except:
            raise
        return dataset, dictkeys

    def write(self, dataset):
        '''
        This function writes data from dataset parameter to the csv file.
        Use this function when data are stored in a matrix.
        
        :Parameters:
        dataset: matrix of the data to store.
        
        '''
        try:
            with open(self.filename, "w", newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=",")
                for row in dataset:
                    writer.writerow(row)
        except:
            raise

    def writeDict(self, dataset, dictkeys):
        '''
        This function writes data from dataset parameter to the csv file.
        Use this function when data are stored in an array of dictionaries.
        
        :Parameters:
        dataset: array of dictionaries where data are stored.
        dictkeys: keys of each dictionary in dataset array.
        
        '''
        try:
            with open(self.filename, "w", newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=dictkeys)
                writer.writeheader()
                for row in dataset:
                    writer.writerow(row)
        except:
            raise
