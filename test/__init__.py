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

import unittest

from utils import ConsistencyCheck

tests = [{
    "ontologyName": "Hotel.owl",
    "ontologyPrefix": "<http://www.semanticweb.org/ontologies/Hotel.owl#>",
    "SPARQLEndPoint": "http://localhost:3030/inf/sparql",
    "domainClasses": ["Bed_and_Breakfast", "Hotel_1_Star"],
    "rangeClasses": ["Square", "Bridge"],
    "objectPropertyToAuxiliaryClass": "hasDistance",
    "auxiliaryClass": "Distance",
    "objectPropertyFromAuxiliaryClass": "isDistanceFor",
    "dataPropertyToFuzzify": "hasValue",
    "fuzzySetLabels": ["Low", "Mid", "High"],
    "quantifiersLabels": ["AlmostNone", "Few", "Some", "Many", "Most"],
    "quantifiersPrototypes": [0.05, 0.275, 0.5, 0.725, 0.95]
},
    {
        "ontologyName": "Hotel.owl",
        "ontologyPrefix": "<http://www.semanticweb.org/ontologies/Hotel.owl#>",
        "SPARQLEndPoint": "http://localhost:3030/inf/sparql",
        "domainClasses": ["Bed_and_Breakfast", "Hotel_1_Star"],
        "rangeClasses": [""],
        "objectPropertyToAuxiliaryClass": "",
        "auxiliaryClass": "",
        "objectPropertyFromAuxiliaryClass": "",
        "dataPropertyToFuzzify": "hasPrice",
        "fuzzySetLabels": ["Low", "Mid", "High"],
        "quantifiersLabels": ["AlmostNone", "Few", "Some", "Many", "Most"],
        "quantifiersPrototypes": [0.05, 0.275, 0.5, 0.725, 0.95]
    },{
    "ontologyName": "Ho#tel.owl",
    "ontologyPrefix": "<http://www.semanticweb.org/ontologies/Hotel.owl#>",
    "SPARQLEndPoint": "http://localhost:3030/inf/sparql",
    "domainClasses": ["Bed_and_Breakfast", "Hotel_1_Star"],
    "rangeClasses": ["Square", "Bridge"],
    "objectPropertyToAuxiliaryClass": "hasDistance",
    "auxiliaryClass": "Distance",
    "objectPropertyFromAuxiliaryClass": "isDistanceFor",
    "dataPropertyToFuzzify": "hasValue",
    "fuzzySetLabels": ["Low", "Mid", "High"],
    "quantifiersLabels": ["AlmostNone", "Few", "Some", "Many", "Most"],
    "quantifiersPrototypes": [0.05, 0.275, 0.5, 0.725, 0.95]
}, {
        "ontologyName": "Hot#el.owl",
        "ontologyPrefix": "<http://www.semanticweb.org/ontologies/Hotel.owl#>",
        "SPARQLEndPoint": "http://localhost:3030/inf/sparql",
        "domainClasses": ["Bed_and_Breakfast", "Hotel_1_Star"],
        "rangeClasses": ["Square", "Bridge"],
        "objectPropertyToAuxiliaryClass": "hasDistance",
        "auxiliaryClass": "Distance",
        "objectPropertyFromAuxiliaryClass": "isDistanceFor",
        "dataPropertyToFuzzify": "hasValue",
        "fuzzySetLabels": ["Low", "Mid", "High"],
        "quantifiersLabels": ["AlmostNone", "Few", "Some", "Many", "Most"],
        "quantifiersPrototypes": [0.05, 0.275, 0.5, 0.725, 0.95]
    }, {
        "ontologyName": "Hotel.owl",
        "ontologyPrefix": "http://www.semanticweb.org/ontologies/Hotel.owl#>",
        "SPARQLEndPoint": "http://localhost:3030/inf/sparql",
        "domainClasses": ["Bed_and_Breakfast", "Hotel_1_Star"],
        "rangeClasses": ["Square", "Bridge"],
        "objectPropertyToAuxiliaryClass": "hasDistance",
        "auxiliaryClass": "Distance",
        "objectPropertyFromAuxiliaryClass": "isDistanceFor",
        "dataPropertyToFuzzify": "hasValue",
        "fuzzySetLabels": ["Low", "Mid", "High"],
        "quantifiersLabels": ["AlmostNone", "Few", "Some", "Many", "Most"],
        "quantifiersPrototypes": [0.05, 0.275, 0.5, 0.725, 0.95]
    }, {
        "ontologyName": "Hotel.owl",
        "ontologyPrefix": "<http://www.semanticweb.org/ontologies/Hotel.owl#>",
        "SPARQLEndPoint": "http:/localhost:3030/inf/sparql",
        "domainClasses": ["Bed_and_Breakfast", "Hotel_1_Star"],
        "rangeClasses": ["Square", "Bridge"],
        "objectPropertyToAuxiliaryClass": "hasDistance",
        "auxiliaryClass": "Distance",
        "objectPropertyFromAuxiliaryClass": "isDistanceFor",
        "dataPropertyToFuzzify": "hasValue",
        "fuzzySetLabels": ["Low", "Mid", "High"],
        "quantifiersLabels": ["AlmostNone", "Few", "Some", "Many", "Most"],
        "quantifiersPrototypes": [0.05, 0.275, 0.5, 0.725, 0.95]
    }, {
        "ontologyName": "Hotel.owl",
        "ontologyPrefix": "<http://www.semanticweb.org/ontologies/Hotel.owl#>",
        "SPARQLEndPoint": "http://localhost:3030/inf/sparql",
        "domainClasses": ["Bed_and_.Breakfast", "Hotel_1_Star"],
        "rangeClasses": ["Square", "Bridge"],
        "objectPropertyToAuxiliaryClass": "hasDistance",
        "auxiliaryClass": "Distance",
        "objectPropertyFromAuxiliaryClass": "isDistanceFor",
        "dataPropertyToFuzzify": "hasValue",
        "fuzzySetLabels": ["Low", "Mid", "High"],
        "quantifiersLabels": ["AlmostNone", "Few", "Some", "Many", "Most"],
        "quantifiersPrototypes": [0.05, 0.275, 0.5, 0.725, 0.95]
    }, {
        "ontologyName": "Hotel.owl",
        "ontologyPrefix": "<http://www.semanticweb.org/ontologies/Hotel.owl#>",
        "SPARQLEndPoint": "http://localhost:3030/inf/sparql",
        "domainClasses": ["Bed_and_Breakfast", "Hotel_1_Star"],
        "rangeClasses": ["Squa[re", "Bridge"],
        "objectPropertyToAuxiliaryClass": "hasDistance",
        "auxiliaryClass": "Distance",
        "objectPropertyFromAuxiliaryClass": "isDistanceFor",
        "dataPropertyToFuzzify": "hasValue",
        "fuzzySetLabels": ["Low", "Mid", "High"],
        "quantifiersLabels": ["AlmostNone", "Few", "Some", "Many", "Most"],
        "quantifiersPrototypes": [0.05, 0.275, 0.5, 0.725, 0.95]
    }, {
        "ontologyName": "Hotel.owl",
        "ontologyPrefix": "<http://www.semanticweb.org/ontologies/Hotel.owl#>",
        "SPARQLEndPoint": "http://localhost:3030/inf/sparql",
        "domainClasses": ["Bed_and_Breakfast", "Hotel_1_Star"],
        "rangeClasses": ["Square", "Bridge"],
        "objectPropertyToAuxiliaryClass": "hasDistan@ce",
        "auxiliaryClass": "Distance",
        "objectPropertyFromAuxiliaryClass": "isDistanceFor",
        "dataPropertyToFuzzify": "hasValue",
        "fuzzySetLabels": ["Low", "Mid", "High"],
        "quantifiersLabels": ["AlmostNone", "Few", "Some", "Many", "Most"],
        "quantifiersPrototypes": [0.05, 0.275, 0.5, 0.725, 0.95]
    }, {
        "ontologyName": "Hotel.owl",
        "ontologyPrefix": "<http://www.semanticweb.org/ontologies/Hotel.owl#>",
        "SPARQLEndPoint": "http://localhost:3030/inf/sparql",
        "domainClasses": ["Bed_and_Breakfast", "Hotel_1_Star"],
        "rangeClasses": ["Square", "Bridge"],
        "objectPropertyToAuxiliaryClass": "hasDistance",
        "auxiliaryClass": "Distan§ce",
        "objectPropertyFromAuxiliaryClass": "isDistanceFor",
        "dataPropertyToFuzzify": "hasValue",
        "fuzzySetLabels": ["Low", "Mid", "High"],
        "quantifiersLabels": ["AlmostNone", "Few", "Some", "Many", "Most"],
        "quantifiersPrototypes": [0.05, 0.275, 0.5, 0.725, 0.95]
    }, {
        "ontologyName": "Hotel.owl",
        "ontologyPrefix": "<http://www.semanticweb.org/ontologies/Hotel.owl#>",
        "SPARQLEndPoint": "http://localhost:3030/inf/sparql",
        "domainClasses": ["Bed_and_Breakfast", "Hotel_1_Star"],
        "rangeClasses": ["Square", "Bridge"],
        "objectPropertyToAuxiliaryClass": "hasDistance",
        "auxiliaryClass": "Distance",
        "objectPropertyFromAuxiliaryClass": "isDistan?ceFor",
        "dataPropertyToFuzzify": "hasValue",
        "fuzzySetLabels": ["Low", "Mid", "High"],
        "quantifiersLabels": ["AlmostNone", "Few", "Some", "Many", "Most"],
        "quantifiersPrototypes": [0.05, 0.275, 0.5, 0.725, 0.95]
    }, {
        "ontologyName": "Hotel.owl",
        "ontologyPrefix": "<http://www.semanticweb.org/ontologies/Hotel.owl#>",
        "SPARQLEndPoint": "http://localhost:3030/inf/sparql",
        "domainClasses": ["Bed_and_Breakfast", "Hotel_1_Star"],
        "rangeClasses": ["Square", "Bridge"],
        "objectPropertyToAuxiliaryClass": "hasDistance",
        "auxiliaryClass": "Distance",
        "objectPropertyFromAuxiliaryClass": "isDistanceFor",
        "dataPropertyToFuzzify": "hasValue(",
        "fuzzySetLabels": ["Low", "Mid", "High"],
        "quantifiersLabels": ["AlmostNone", "Few", "Some", "Many", "Most"],
        "quantifiersPrototypes": [0.05, 0.275, 0.5, 0.725, 0.95]
    }, {
        "ontologyName": "Hotel.owl",
        "ontologyPrefix": "<http://www.semanticweb.org/ontologies/Hotel.owl#>",
        "SPARQLEndPoint": "http://localhost:3030/inf/sparql",
        "domainClasses": ["Bed_and_Breakfast", "Hotel_1_Star"],
        "rangeClasses": ["Square", "Bridge"],
        "objectPropertyToAuxiliaryClass": "hasDistance",
        "auxiliaryClass": "Distance",
        "objectPropertyFromAuxiliaryClass": "isDistanceFor",
        "dataPropertyToFuzzify": "hasValue",
        "fuzzySetLabels": [""],
        "quantifiersLabels": ["AlmostNone", "Few", "Some", "Many", "Most"],
        "quantifiersPrototypes": [0.05, 0.275, 0.5, 0.725, 0.95]
    }, {
        "ontologyName": "Hotel.owl",
        "ontologyPrefix": "<http://www.semanticweb.org/ontologies/Hotel.owl#>",
        "SPARQLEndPoint": "http://localhost:3030/inf/sparql",
        "domainClasses": ["Bed_and_Breakfast", "Hotel_1_Star"],
        "rangeClasses": ["Square", "Bridge"],
        "objectPropertyToAuxiliaryClass": "hasDistance",
        "auxiliaryClass": "Distance",
        "objectPropertyFromAuxiliaryClass": "isDistanceFor",
        "dataPropertyToFuzzify": "hasValue",
        "fuzzySetLabels": ["Low"],
        "quantifiersLabels": ["AlmostNone", "Few", "Some", "Many", "Most"],
        "quantifiersPrototypes": [0.05, 0.275, 0.5, 0.725, 0.95]
    }, {
        "ontologyName": "Hotel.owl",
        "ontologyPrefix": "<http://www.semanticweb.org/ontologies/Hotel.owl#>",
        "SPARQLEndPoint": "http://localhost:3030/inf/sparql",
        "domainClasses": ["Bed_and_Breakfast", "Hotel_1_Star"],
        "rangeClasses": ["Square", "Bridge"],
        "objectPropertyToAuxiliaryClass": "hasDistance",
        "auxiliaryClass": "Distance",
        "objectPropertyFromAuxiliaryClass": "isDistanceFor",
        "dataPropertyToFuzzify": "hasValue",
        "fuzzySetLabels": ["Low", "Mi;d", "High"],
        "quantifiersLabels": ["AlmostNone", "Few", "Some", "Many", "Most"],
        "quantifiersPrototypes": [0.05, 0.275, 0.5, 0.725, 0.95]
    }, {
        "ontologyName": "Hotel.owl",
        "ontologyPrefix": "<http://www.semanticweb.org/ontologies/Hotel.owl#>",
        "SPARQLEndPoint": "http://localhost:3030/inf/sparql",
        "domainClasses": ["Bed_and_Breakfast", "Hotel_1_Star"],
        "rangeClasses": ["Square", "Bridge"],
        "objectPropertyToAuxiliaryClass": "hasDistance",
        "auxiliaryClass": "Distance",
        "objectPropertyFromAuxiliaryClass": "isDistanceFor",
        "dataPropertyToFuzzify": "hasValue",
        "fuzzySetLabels": ["Low", "Mid", "High"],
        "quantifiersLabels": ["AlmostNone", "Few", "Some", "Many"],
        "quantifiersPrototypes": [0.05, 0.275, 0.5, 0.725, 0.95]
    }, {
        "ontologyName": "Hotel.owl",
        "ontologyPrefix": "<http://www.semanticweb.org/ontologies/Hotel.owl#>",
        "SPARQLEndPoint": "http://localhost:3030/inf/sparql",
        "domainClasses": ["Bed_and_Breakfast", "Hotel_1_Star"],
        "rangeClasses": ["Square", "Bridge"],
        "objectPropertyToAuxiliaryClass": "hasDistance",
        "auxiliaryClass": "Distance",
        "objectPropertyFromAuxiliaryClass": "isDistanceFor",
        "dataPropertyToFuzzify": "hasValue",
        "fuzzySetLabels": ["Low", "Mid", "High"],
        "quantifiersLabels": ["AlmostNone", "Few", "Some", "Ma#ny", "Most"],
        "quantifiersPrototypes": [0.05, 0.275, 0.5, 0.725, 0.95]
    }, {
        "ontologyName": "Hotel.owl",
        "ontologyPrefix": "<http://www.semanticweb.org/ontologies/Hotel.owl#>",
        "SPARQLEndPoint": "http://localhost:3030/inf/sparql",
        "domainClasses": ["Bed_and_Breakfast", "Hotel_1_Star"],
        "rangeClasses": ["Square", "Bridge"],
        "objectPropertyToAuxiliaryClass": "hasDistance",
        "auxiliaryClass": "Distance",
        "objectPropertyFromAuxiliaryClass": "isDistanceFor",
        "dataPropertyToFuzzify": "hasValue",
        "fuzzySetLabels": ["Low", "Mid", "High"],
        "quantifiersLabels": ["AlmostNone"],
        "quantifiersPrototypes": [0.05]
    }, {
        "ontologyName": "Hotel.owl",
        "ontologyPrefix": "<http://www.semanticweb.org/ontologies/Hotel.owl#>",
        "SPARQLEndPoint": "http://localhost:3030/inf/sparql",
        "domainClasses": ["Bed_and_Breakfast", "Hotel_1_Star"],
        "rangeClasses": ["Square", "Bridge"],
        "objectPropertyToAuxiliaryClass": "hasDistance",
        "auxiliaryClass": "Distance",
        "objectPropertyFromAuxiliaryClass": "isDistanceFor",
        "dataPropertyToFuzzify": "hasValue",
        "fuzzySetLabels": ["Low", "Mid", "High"],
        "quantifiersLabels": ["AlmostNone", "Few", "Some", "Many", "Most"],
        "quantifiersPrototypes": [0.05, 0.275, 0.725, 0.5, 0.95]
    }, {
        "ontologyName": "Hotel.owl",
        "ontologyPrefix": "<http://www.semanticweb.org/ontologies/Hotel.owl#>",
        "SPARQLEndPoint": "http://localhost:3030/inf/sparql",
        "domainClasses": ["Bed_and_Breakfast", "Hotel_1_Star"],
        "rangeClasses": ["Square", "Bridge"],
        "objectPropertyToAuxiliaryClass": "hasDistance",
        "auxiliaryClass": "Distance",
        "objectPropertyFromAuxiliaryClass": "isDistanceFor",
        "dataPropertyToFuzzify": "hasValue",
        "fuzzySetLabels": ["Low", "Mid", "High"],
        "quantifiersLabels": ["AlmostNone", "Few", "Some", "Many", "Most"],
        "quantifiersPrototypes": [0.05, "0.2475", 0.725, 0.5, 0.95]
    }]

expected = [True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]

class TestConsistencyCheck(unittest.TestCase):
    def test(self):
        i = 1
        for test in tests:
            c = ConsistencyCheck(test)
            self.assertEquals(c(), expected[i-1], "Something went wrong with test #" + str(i))
            i += 1


if __name__ == '__main__':
    unittest.main()
