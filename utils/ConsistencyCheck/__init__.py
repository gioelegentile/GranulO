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
import re


class ConsistencyCheck(object):
    """
    This class provides to check the consistency of data input from config.json configuration file
    """

    def __init__(self, data):
        self.ontologyname = data["ontologyName"]
        self.ontologyprefix = data["ontologyPrefix"]
        self.sparqlendpoint = data["SPARQLEndPoint"]
        self.domainclasses = data["domainClasses"]
        self.rangeclasses = data["rangeClasses"]
        self.objectpropertytoauxiliaryclass = data["objectPropertyToAuxiliaryClass"]
        self.auxiliaryclass = data["auxiliaryClass"]
        self.objectpropertyfromauxiliaryclass = data["objectPropertyFromAuxiliaryClass"]
        self.datapropertytofuzzify = data["dataPropertyToFuzzify"]
        self.fuzzysetlabels = data["fuzzySetsLabels"]
        self.quantifierslabels = data["quantifiersLabels"]
        self.quantifiersprototypes = data["quantifiersPrototypes"]

    def __call__(self):
        if (self.sparqlendpoint != "" and self.ontologyprefix != "" and self.ontologyname != "" and
                self.domainclasses != [""] and self.datapropertytofuzzify != "" and self.fuzzysetlabels != "" and
                self.quantifierslabels != "" and self.quantifiersprototypes != "" and
                ((self.objectpropertytoauxiliaryclass == "" and self.objectpropertyfromauxiliaryclass == "" and
                    self.auxiliaryclass == "" and self.rangeclasses == [""]) or (
                    self.objectpropertytoauxiliaryclass != "" and self.objectpropertyfromauxiliaryclass != "" and
                    self.auxiliaryclass != "" and self.rangeclasses != [""]))):
            checked = True
            if not ConsistencyCheck.checkontologyname(self):
                logging.warning("'ontologyName' syntax is wrong.")
                checked = False
            if not ConsistencyCheck.checkontolofyprefix(self):
                logging.warning("'ontologyPrefix' syntax is wrong.")
                checked = False
            if not ConsistencyCheck.checksparqlendpoint(self):
                logging.warning("'SPARQLEndPoint' syntax is wrong.")
                checked = False
            if not ConsistencyCheck.checklistnames(self.domainclasses):
                checked = False
            if not ConsistencyCheck.checklistnames(self.rangeclasses):
                checked = False
            if not ConsistencyCheck.checkname(self.objectpropertytoauxiliaryclass):
                logging.warning("'objectPropertyToAuxiliaryClass' syntax is wrong.")
                checked = False
            if not ConsistencyCheck.checkname(self.auxiliaryclass):
                logging.warning("'auxiliaryClass' syntax is wrong.")
                checked = False
            if not ConsistencyCheck.checkname(self.objectpropertyfromauxiliaryclass):
                logging.warning("'objectPropertyFromAuxiliaryClass' syntax is wrong.")
                checked = False
            if not ConsistencyCheck.checkname(self.datapropertytofuzzify):
                logging.warning("'dataPropertyToFuzzify' syntax is wrong.")
                checked = False
            if not ConsistencyCheck.checkfuzzysetlabels(self):
                checked = False
            if not ConsistencyCheck.checkquantifiers(self):
                checked = False
            return checked
        else:
            logging.warning("ERROR: the parameters in the configuration file (config.json) are not setted in the right "
                            "way.")
            return False

    def checkontologyname(self):
        return re.match("^[A-Za-z0-9_.-]*.owl$", self.ontologyname)

    def checkontolofyprefix(self):
        return re.match("^<http://[A-Za-z0-9_.:/-]*#>$", self.ontologyprefix)

    def checksparqlendpoint(self):
        return re.match("^http://[A-Za-z0-9_.:/-]*$", self.sparqlendpoint)

    def checkname(str):
        return re.match("^[A-Za-z0-9_-]*$", str)

    def checkfuzzysetlabels(self):
        if len(self.fuzzysetlabels) > 1:
            return ConsistencyCheck.checklistnames(self.fuzzysetlabels)
        else:
            logging.warning("'fuzzySetLabels' length must be > 1.")
            return False

    def checklistnames(list):
        for name in list:
            if not ConsistencyCheck.checkname(name):
                logging.warning("'" + name + "' syntax is wrong.")
                return False
        return True

    def checkquantifiers(self):
        check = True
        if not len(self.quantifierslabels) == len(self.quantifiersprototypes):
            logging.warning("'quantifiersLabels' and 'quantifiersPrototypes' must have the same length")
            check = False
        if not (len(self.quantifierslabels) > 1 and len(self.quantifiersprototypes) > 1):
            logging.warning("'quantifiersLabels' and 'quantifiersPrototypes' must have length > 1")
            check = False
        if not ConsistencyCheck.checkquantifiersprototypes(self):
            check = False
        elif not ConsistencyCheck.checkifquantifiersprototypesaresorted(self):
            check = False
        if not ConsistencyCheck.checklistnames(self.quantifierslabels):
            check = False
        return check

    def checkifquantifiersprototypesaresorted(self):
        if all(self.quantifiersprototypes[i] <= self.quantifiersprototypes[i + 1] for i in
               range(len(self.quantifiersprototypes) - 1)):
            return True
        else:
            logging.warning("'quantifiersPrototypes' are not sorted.")

    def checkquantifiersprototypes(self):
        for s in self.quantifiersprototypes:
            if not isinstance(s, float):
                logging.warning("'" + s + "' is not a number.")
                return False
        return True
