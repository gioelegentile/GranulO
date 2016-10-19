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

from os.path import exists as file_exists


class FileHandler(object):
    '''
    This class provides functions to read/write informations from/into files.
    '''

    def __init__(self, filename):
        '''
        Initializes the instances of the class
        
        :Parameters:
        filename: name of the file to open.
        
        '''
        self.filename = filename

    def append(self, data):
        '''
        This function appends data into the file.
        
        :Parameters:
        data: string of data to append.
        
        '''
        try:
            with open(self.filename, "a") as file:
                file.write(data)
        except:
            raise

    def exists(self):
        '''
        This function verify if the file exists.
        
        :Returns:
        True if the file exists, else returns False
        
        '''
        return file_exists(self.filename)

    def readAll(self):
        '''
        This function reads data from the file.
        
        :Returns:
        data: list of the lines read from the file.
        
        '''
        data = []
        try:
            with open(self.filename, "r") as file:
                data = file.readlines()
        except:
            raise
        return data

    def writeAll(self, data):
        '''
        This function writes data in the file.
        
        :Parameters:
        data: list of data to write.
        
        '''
        try:
            with open(self.filename, "w") as file:
                file.writelines(data)
        except:
            raise
