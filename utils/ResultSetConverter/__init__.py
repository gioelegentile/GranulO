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

def convertToLD(resultset):
    '''
    This function converts the result-set in a list. Each list's row is a
    dictionary, where the keys are required fields of the result-set.

    :Returns:
    array: list of data extracted from result-set; in each row of array
           there is a dictionary that represents the tuples;
           keys: list of dictionaries keys that represent the fields of tuple.

    '''
    result = resultset["results"]["bindings"]
    array = []
    keys = []
    if result:
        keys = [key for key in result[0].keys()]
        array = [{key: row[key]["value"] for key in keys} for row in result]
    return array, keys


def convertToListOfDict(resultset):
    '''
    This function converts the result-set in a list. Each list's row is a
    dictionary, where the keys are required fields of the result-set.

    :Returns:
    array: list of data extracted from result-set; in each row of array
           there is a dictionary that represents the tuples;
           keys: list of dictionaries keys that represent the fields of tuple.

    '''
    result = resultset["results"]["bindings"]
    array = []
    array1 = []
    keys = []
    keyNew = []
    if result:
        keys = [key for key in result[0].keys()]
        for row in result:
            if len(row) != len(keys):
                keyNew = [key for key in row.keys()]
                break
            else:
                keyNew = keys
                break

                # for row in result:
                # for key in keys:
                # if row[key]["value"]!=None:
                # array.append({key: row[key]["value"]})
        array = [{key: row[key]["value"] for key in keys} for row in result if len(row) == len(keys)]
        array1 = [{key: row[key]["value"] for key in keyNew} for row in result if len(row) != len(keys)]
        array2 = [{key: row[key]["value"] for key in keyNew} for row in result]  # array diverso da result
        array1.extend(array2)
    return array, array1, keys, keyNew


def convertToMatrix(resultset):
    '''
    This function converts the result-set in a matrix. Each matrix's row
    is an array of tuples.

    :Returns:
    array: the matrix of data extracted from result-set.

    '''
    result = resultset["results"]["bindings"]
    array = []
    if result:
        array = [[row[col]["value"] for col in row] for row in result]
    return array
