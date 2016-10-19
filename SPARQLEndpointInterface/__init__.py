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

from SPARQLWrapper import SPARQLWrapper, JSON


class SPARQLEndpointInterface(object):
    '''
    This class is an interface that uses "SPARQLWrapper" library as default
    SPARQL end-point interface.
    '''

    def __init__(self, uri):
        '''
        Initializes the instance of the class.
        
        :Parameters:
        uri: the uri of the ontology to query.
        
        '''
        self._sparql = SPARQLWrapper(uri)

    def __call__(self, statement):
        '''
        This function sends the query to the SPARQL end-point.
        
        :Parameter:
        statement: query in string form to send.
        
        :Returns:
        resultset: the result-set list in JSON format.
        
        '''
        resultset = []
        self._sparql.setQuery(statement)
        self._sparql.setReturnFormat(JSON)
        logging.warning("\nSPARQLInterface is executing the following query...")
        logging.warning(statement)
        try:
            t0 = time()
            rs = self._sparql.query()
            tf = time()
            resultset = rs.convert()
            logging.warning("Query has been executed in {0:.3f} seconds!".format(tf - t0))
        except:
            raise
        self._sparql.resetQuery()
        logging.warning("Result:")
        logging.warning(resultset)
        return resultset
