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

import datetime
import json
import logging
import os
import shutil
from re import findall
from time import time

from FuzzyClustering import FuzzyClustering
from FuzzyGranulation import FuzzyGranulation
from FuzzyQuantification import FuzzyQuantification
from OWLOntology import OWLOntology
from SPARQLEndpointInterface import SPARQLEndpointInterface
from utils import CSVHandler, ConsistencyCheck, ResultSetConverter, convertToListOfDict as converter


class Main:
    _time = ""
    _index = 1


def executeQuery(SPARQLEndpoint, ontologyPrefix, dataPropertyToFuzzify, domainClass, rangeClass="", auxiliaryClass="",
                 objectProperty=""):
    """
    Executes the SPARQL query and stores the resultset in a csv file. It has a different behaviour based on the input
    parameters. If rangeClass, auxiliaryClass, objectProperty and dataPropertyToFuzzify are not blank, the
    operation is ternary; binary, otherwise.

    :param SPARQLEndpoint: the SPARQL end point
    :param ontologyPrefix: the ontology prefix
    :param domainClass: the domain class
    :param dataPropertyToFuzzify: the data property to fuzzify
    :param rangeClass: the range class
    :param auxiliaryClass: the auxiliar class
    :param objectProperty: the object property
    """
    nameProperty = createNameProperty(dataPropertyToFuzzify)

    # obtain a connection to the endpoint
    sparql = SPARQLEndpointInterface(SPARQLEndpoint)

    targetDomainClass = ""
    targetRangeClass = ""
    targetauxiliaryClass = ""
    targetdataPropertyToFuzzify = ""

    if rangeClass == "" and auxiliaryClass == "" and objectProperty == ["", ""]:
        targetDomainClass = " ?" + domainClass
        targetdataPropertyToFuzzify = " ?" + nameProperty
        whereClause = "  ?" + domainClass + " a ontology:" + domainClass + ". ?" + domainClass + " ontology:" + dataPropertyToFuzzify + " ?" + nameProperty
    elif rangeClass != "" and auxiliaryClass != "" and objectProperty != ["", ""]:
        targetDomainClass = " ?" + domainClass
        targetRangeClass = " ?" + rangeClass
        targetauxiliaryClass = " ?" + auxiliaryClass
        targetdataPropertyToFuzzify = " ?" + nameProperty
        whereClause = "?" + domainClass + " a ontology:" + domainClass + ". ?" + rangeClass + " a ontology:" + rangeClass + ".  ?" + domainClass + " ontology:" + \
                      objectProperty[0] + " ?" + auxiliaryClass + ".  ?" + auxiliaryClass + " ontology:" + \
                      objectProperty[
                          1] + " ?" + rangeClass + ". ?" + auxiliaryClass + " ontology:" + dataPropertyToFuzzify + " ?" + nameProperty

    query = ("PREFIX ontology: " + ontologyPrefix +
             " SELECT " + targetDomainClass + targetRangeClass + targetauxiliaryClass + targetdataPropertyToFuzzify +
             "    WHERE { "
             + whereClause + "}")

    # sends the query
    rs, rs2, fields, fields2 = converter(sparql(query))
    resultset = []

    # store only the identifiers of generic class
    if rangeClass == "" and auxiliaryClass == "" and objectProperty == ["", ""]:
        resultset = [{domainClass: row.get(domainClass).split("#", 1)[1], nameProperty: row.get(nameProperty)} for
                     row
                     in rs2]
        # save the resultset in the csv file
        if not resultset == []:
            if not os.path.exists('output/' + Main._time + '/csv_files/'):
                os.makedirs('output/' + Main._time + '/csv_files/')
            csvhandler = CSVHandler('output/' + Main._time + '/csv_files/' + domainClass + ".csv")
            csvhandler.writeDict(resultset, fields2)
    elif rangeClass != "" and auxiliaryClass != "" and objectProperty != ["", ""]:
        resultset = [
            {domainClass: row.get(domainClass).split("#", 1)[1],
             auxiliaryClass: row.get(auxiliaryClass).split("#", 1)[1],
             rangeClass: row.get(rangeClass).split("#", 1)[1], nameProperty: row.get(nameProperty)}
            for
            row in rs]
        # save the resultset in the csv file
        if not resultset == []:
            if not os.path.exists('output/' + Main._time + '/csv_files/'):
                os.makedirs('output/' + Main._time + '/csv_files/')
            csvhandler = CSVHandler(
                'output/' + Main._time + '/csv_files/' + auxiliaryClass + domainClass + rangeClass + ".csv")
            csvhandler.writeDict(resultset, fields)

    if resultset == []:
        logging.warning("\nSomething went wrong with the query:\n\n" + query)
        raise Exception


def clustering(numclusters, dataPropertyToFuzzify, domainClass, rangeClass="", auxiliaryClass=""):
    """
    Executes the fuzzy clustering using C-Means algorithm and stores the result (sorted centroids) in a csv file.

    :param numclusters: the clusters number
    :param dataPropertyToFuzzify: the data property to fuzzify
    :param domainClass: the domain class
    :param rangeClass: the range class (blank if the operation is binary)
    :param auxiliaryClass: the auxiliar class (blank if the operation is binary)
    """
    nameProperty = createNameProperty(dataPropertyToFuzzify)

    # get individuals and their values from csv file
    csvhandler = CSVHandler('output/' + Main._time + '/csv_files/' + auxiliaryClass + domainClass + rangeClass + ".csv")
    d, _ = csvhandler.readDict()
    dataset = [[float(r.get(nameProperty))] for r in d]

    # execute the process of fuzzy clustering and get the clusters centroids
    fc = FuzzyClustering(trainingset=dataset, clusters=numclusters)
    centers = sorted(fc())

    # store centroid in centroids.csv
    csvhandler = CSVHandler(
        'output/' + Main._time + '/csv_files/' + auxiliaryClass + domainClass + rangeClass + "Centroids.csv")
    csvhandler.write(centers)

    logging.warning("Centroids result of clustering process:")
    logging.warning(centers)


def granulation(labels, dataPropertyToFuzzify, domainClass, rangeClass="", auxiliaryClass=""):
    """
    Executes the granulation and stores the result in a csv file. It takes the centroids from the csv file calculated
    with clustering function. It also stores the graphs of Strong Fuzzy Partition and the result of granulation.

    :param labels: the labels list
    :param dataPropertyToFuzzify: the data property to fuzzify
    :param domainClass: the domain class
    :param rangeClass: the range class (if empty, the operation is binary)
    :param auxiliaryClass: the auxiliar class (if empty, the operation is binary)
    """
    nameProperty = createNameProperty(dataPropertyToFuzzify)

    # get centroids from centroids.csv
    csvhandler = CSVHandler(
        'output/' + Main._time + '/csv_files/' + auxiliaryClass + domainClass + rangeClass + "Centroids.csv")
    centers = csvhandler.read()

    quantifierPrototypes = [float(c[0]) for c in centers]

    # get general class dataPropertyToFuzzify from csv file
    csvhandler = CSVHandler('output/' + Main._time + '/csv_files/' + auxiliaryClass + domainClass + rangeClass + ".csv")
    d, _ = csvhandler.readDict()
    dataset = [float(r.get(nameProperty)) for r in d]

    # execute the process of fuzzy granulation and store the results
    fuzzygranulation = FuzzyGranulation(dataset, quantifierPrototypes, labels)
    table = fuzzygranulation()

    # plot the SFP
    if not os.path.exists('output/' + Main._time + '/graphs'):
        os.makedirs('output/' + Main._time + '/graphs')
    fuzzygranulation.plotSFP("quantifierPrototypes", "Fuzzy membership",
                             'output/' + Main._time + '/graphs/' + auxiliaryClass + domainClass + rangeClass)

    # plot the result of granulation
    if rangeClass == "" and auxiliaryClass == "":
        fuzzygranulation.plot(domainClass + " " + nameProperty, "Fuzzy membership",
                              'output/' + Main._time + '/graphs/' + domainClass,
                              "Classification of " + domainClass + " by " + nameProperty)
    else:
        fuzzygranulation.plot(auxiliaryClass + " " + nameProperty, "Fuzzy membership",
                              'output/' + Main._time + '/graphs/' + auxiliaryClass + domainClass + rangeClass,
                              "Classification of " + domainClass + " by " + auxiliaryClass + " from " + rangeClass)

    # organize the results in order to save them in the csv file
    element = domainClass if (rangeClass == "" and auxiliaryClass == "") else auxiliaryClass
    header = [element, nameProperty]
    header.extend(labels)
    matrix = []
    for Element, memberships in zip(d, [ms for (_, ms) in table]):
        row = {element: Element.get(element), nameProperty: Element.get(nameProperty)}
        for label, degree in memberships:
            row.setdefault(label, degree)
        matrix.append(row)

    # save the results in granules.csv
    csvhandler = CSVHandler('output/' + Main._time + '/csv_files/' + auxiliaryClass + domainClass + rangeClass +
                            "Granules.csv")
    csvhandler.writeDict(matrix, header)

    logging.warning("Matrix result of granulation process:")
    logging.warning(matrix)


def quantification(quantifierLabels, quantifierPrototypes, dataPropertyToFuzzify, domainClass, rangeClass="",
                   auxiliaryClass=""):
    """
    Execute the quantification using FuzzyQuantification class. Stores the results in a csv file.

    :param quantifierLabels: the quantifier labels
    :param quantifierPrototypes: the quantifier prototypes
    :param dataPropertyToFuzzify: the data property to fuzzify
    :param domainClass: the domain class
    :param rangeClass: the range class (if empty, the operation is binary)
    :param auxiliaryClass: the auxiliary class (if empty, the operation is binary)
    """
    nameProperty = createNameProperty(dataPropertyToFuzzify)

    # get the granules from granules.csv
    csvhandler = CSVHandler(
        'output/' + Main._time + '/csv_files/' + auxiliaryClass + domainClass + rangeClass + "Granules.csv")
    ds, granuleslabels = csvhandler.readDict()
    granuleslabels = granuleslabels[2:]
    granules = [{label: float(row.get(label)) for label in granuleslabels} for row in ds]

    # execute the process of fuzzy quantification and get the results
    fuzzyquantification = FuzzyQuantification(quantifierPrototypes, quantifierLabels, granules, granuleslabels)
    quantification = fuzzyquantification()

    # plot the quantifiers
    fuzzyquantification.plotQuantifiers("quantifierPrototypes", "Fuzzy membership",
                                        'output/' + Main._time + '/graphs/' + auxiliaryClass + domainClass + rangeClass)

    # plot the cardinalities
    if rangeClass == "" and auxiliaryClass == "":
        fuzzyquantification \
            .plotCardinalities(domainClass + " Granule cardinality", "Quantifier membership",
                               "Quantification of " + domainClass + " by " + nameProperty,
                               'output/' + Main._time + '/graphs/' + domainClass)

    else:
        fuzzyquantification \
            .plotCardinalities(auxiliaryClass + " Granule cardinality", "Quantifier membership",
                               "Quantification of " + domainClass + " by " + auxiliaryClass + " from " + rangeClass,
                               'output/' + Main._time + '/graphs/' + auxiliaryClass + domainClass + rangeClass)

    # organize the results in order to save them in the csv file
    header = ["granules"]
    header.extend(quantifierLabels)
    matrix = [header]
    for granule in granuleslabels:
        quants = quantification.get(granule)
        row = [granule]
        row.extend([quants.get(quant) for quant in quantifierLabels])
        matrix.append(row)

    # save the results in quantifiers.csv
    csvhandler = CSVHandler(
        'output/' + Main._time + '/csv_files/' + auxiliaryClass + domainClass + rangeClass + "Quantifiers.csv")
    csvhandler.write(matrix)

    # Get the value of sigma-count for every fuzzy sets of granules.
    header = ["granule", "sigma-count"]
    cardinalities = [{"granule": granule, "sigma-count": cardinality}
                     for granule, cardinality in fuzzyquantification.cardinalities.items()]

    # Save cardinalities in cardinalities.csv.
    csvhandler = CSVHandler(
        'output/' + Main._time + '/csv_files/' + auxiliaryClass + domainClass + rangeClass + "Cardinalities.csv")
    csvhandler.writeDict(cardinalities, header)

    logging.warning("Results of quantification process:")
    logging.warning("Matrix:")
    logging.warning(matrix)
    logging.warning("Cardinalities:")
    logging.warning(cardinalities)


def integration(ontologyName, dataPropertyToFuzzify, domainClassesList, rangeClassesList="", auxiliaryClass="",
                objectProperty=""):
    """
    Integrates the results in the original ontology. It picks up the results from previously generated cvs files.

    :param ontologyName: the ontology name
    :param dataPropertyToFuzzify: the data property to fuzzify
    :param domainClassesList: the domain classes list
    :param rangeClassesList: the range classes list (if empty, the operation is binary)
    :param auxiliaryClass: the auxiliary class (if empty, the operation is binary)
    :param objectProperty: the object property (if empty, the operation is binary)
    """
    logging.warning("Integration process in execution...")
    t0 = time()
    nameProperty = createNameProperty(dataPropertyToFuzzify)
    dataPropertyToFuzzify = "g_" + dataPropertyToFuzzify

    # Define acronym() function. It's used to get upper case characters into a string and then to convert them in lower case.
    acronym = lambda string: "".join(findall("[A-Z]", string)).lower()

    # Define trim() function. It's used to purge strings from whitespace character.
    trim = lambda string: string.replace(" ", "")

    # Define Round() function. It's used to round a decimal value and convert it to string format.
    Round = lambda value, pos=3: ("{0:.%df}" % pos).format(value)

    # Set minimum and maximum value.
    k1, k2 = 0, 1000

    # Open ontology.
    ontology = OWLOntology("ontologies/" + ontologyName)

    # Create a copy of original ontology. New axioms will be written in g"onotologyName".owl
    ontology.createBackup('output/' + Main._time + '/g_' + ontologyName)

    countGranule = 0

    if rangeClassesList == [""] and auxiliaryClass == "" and objectProperty == ["", ""]:

        for inheritanceClass in domainClassesList:

            # Get list of centroids from centroids.csv.
            csvhandler = CSVHandler('output/' + Main._time + '/csv_files/' + inheritanceClass + "Centroids.csv")
            centroids = csvhandler.read()
            quantifierPrototypes = [float(c[0]) for c in centroids]

            # Get number of quantifierPrototypes.
            N = len(quantifierPrototypes)

            # Get granules from granules.csv.
            csvhandler = CSVHandler('output/' + Main._time + '/csv_files/' + inheritanceClass + "Granules.csv")
            granules, glabels = csvhandler.readDict()
            glabels.remove(inheritanceClass)
            glabels.remove(nameProperty)

            # Get granules cardinalities from cardinalities.csv.
            csvhandler = CSVHandler('output/' + Main._time + '/csv_files/' + inheritanceClass + "Cardinalities.csv")
            cardinalities, _ = csvhandler.readDict()

            # Get quantifiers from quantifiers.csv.
            csvhandler = CSVHandler('output/' + Main._time + '/csv_files/' + inheritanceClass + "Quantifiers.csv")
            quantifiers, qlabels = csvhandler.readDict()
            qlabels.remove("granules")

            # Add fuzzy granules as OWL classes, where each identifier is extracted from glabels list.
            for granule in glabels:
                ontology.addClass(trim(granule))

            # Add data property as object property.
            ontology.addObjectProperty(dataPropertyToFuzzify)
            ontology.addObjectPropertyDomain(dataPropertyToFuzzify, inheritanceClass)

            # Add domain class subclasses. Every subclass name is extracted from glabels list and concatenated with name property and name domain class string.
            for granule in glabels:
                label = trim(granule) + nameProperty + inheritanceClass
                ontology.addClass(label)
                # Every domain class subclass is defined as intersection between domain class and individual class obtained from existential quantifier restriction.
                someValues1 = ontology.objectSomeValuesFromAxiom(dataPropertyToFuzzify, trim(granule))
                intersectionAxiom = ontology.objectIntersectionOfAxiom(inheritanceClass, someValues1)
                ontology.addEquivalentClasses(label, intersectionAxiom)

            # Add Granule class with individuals defined as acronyms of glabels items
            listGranule = []
            dictGranule = {}
            for i in range(1, len(glabels) + 1):
                countGranule = countGranule + 1
                listGranule.append("granule" + str(countGranule))

            # Add class Granule
            dictGranule[inheritanceClass] = listGranule
            ontology.addClass("Granule", listGranule)

            # Add left-shoulder fuzzy datatype using FuzzyOWL2 formalism.
            annotation = ("<fuzzyOwl2 fuzzyType=\"datatype\">"
                          "<Datatype type=\"leftshoulder\" a=\"{0}\" b=\"{1}\"/>"
                          "</fuzzyOwl2>").format(quantifierPrototypes[0], quantifierPrototypes[1])
            restriction = ontology.datatypeFacetRestrictionAxiom("double", "minInclusive", k1, "maxInclusive", k2)
            ontology.addDatatypeDefinition(trim(glabels[0]), restriction, annotation)

            # For every triangular fuzzy set, add triangular fuzzy datatype using FuzzyOWL2 formalism.
            for i in range(1, N - 1):
                annotation = ("<fuzzyOwl2 fuzzyType=\"datatype\">"
                              "<Datatype type=\"triangular\" a=\"{0}\" b=\"{1}\" c=\"{2}\"/>"
                              "</fuzzyOwl2>").format(quantifierPrototypes[i - 1], quantifierPrototypes[i],
                                                     quantifierPrototypes[i + 1])
                ontology.addDatatypeDefinition(trim(glabels[0]), restriction, annotation)

            # Add right-shoulder fuzzy datatype using FuzzyOWL2 formalism.
            annotation = ("<fuzzyOwl2 fuzzyType=\"datatype\">"
                          "<Datatype type=\"rightshoulder\" a=\"{0}\" b=\"{1}\"/>"
                          "</fuzzyOwl2>").format(quantifierPrototypes[N - 2], quantifierPrototypes[N - 1])
            ontology.addDatatypeDefinition(trim(glabels[0]), restriction, annotation)

            # Add mapsTo object property.
            ontology.addObjectProperty("mapsTo")

            # Every individual of domain class is defined in relative domain class subclasses and mapped with relative granules.
            # The membership degree is represented using FuzzyOWL2 code written into an annotation property.

            for row in granules:
                i = 0
                for granule in glabels:
                    i = i + 1
                    label = trim(granule) + nameProperty + inheritanceClass
                    subClass = row.get(inheritanceClass)
                    degree = float(row.get(granule))
                    if degree > 0:
                        annotation = "<fuzzyOwl2 fuzzyType=\"axiom\"><Degree value=\"{}\"/></fuzzyOwl2>".format(
                            degree)
                        ontology.addIndividual(subClass, label, annotation)
                        ontology.addObjectProperty("mapsTo", subClass, dictGranule.get(inheritanceClass)[i - 1])

            # Add fuzzy quantifiers as Quantifiers subclasses. Every subclass is extracted from qlabels list.
            ontology.addClass("Quantifier")
            for label in qlabels:
                ontology.addClass(trim(label))
                ontology.addSubClass(trim(label), "Quantifier")

            # Define hasCardinality as functional datatype property with domain class "Granule" and range in double datatype.
            ontology.addDatatypeProperty("hasCardinality")
            ontology.addDatatypePropertyDomain("hasCardinality", "Granule")
            ontology.addDatatypePropertyRange("hasCardinality", "double")
            ontology.addFunctionalDatatypeProperty("hasCardinality")

            # Add hasCardinality datatype property that put in relationship Granule's individuals with their sigma-count values.
            for row in cardinalities:
                i = 0
                for label in glabels:
                    i = i + 1
                    if row.get("granule") == label:
                        granule = dictGranule.get(inheritanceClass)[i - 1]
                sigmacount = float(row.get("sigma-count"))
                ontology.addDatatypeProperty("hasCardinality", granule, "double", Round(sigmacount))

            # Add hasCardinality object property.
            ontology.addObjectProperty("g_hasCardinality")
            ontology.addObjectPropertyDomain("g_hasCardinality", "Granule")
            ontology.addObjectPropertyRange("g_hasCardinality", "Quantifier")

            # Every granule is connected with relative quantifier class.
            for row in quantifiers:
                for label in qlabels:
                    i = 0
                    for l in glabels:
                        i = i + 1
                        if row.get("granules") == l:
                            granule = dictGranule.get(inheritanceClass)[i - 1]
                    degree = float(row.get(label))
                    if degree > 0:
                        # The membership degree is represented using FuzzyOWL2 code written into an annotation property.
                        annotation = ontology.fuzzyLabelAnnotation(
                            "<fuzzyOwl2><Degree value=\"{}\"/></fuzzyOwl2>".format(degree))
                        # Define the existential restriction (hasCardinality some <<label>>)
                        someValues = ontology.objectSomeValuesFromAxiom("g_hasCardinality", trim(label))
                        # <<granule>> is an individual of class obtained from existential property (hasCardinality some <<label>>)
                        assertion = "\n\t<ClassAssertion>{0}{1}\n\t\t<NamedIndividual IRI=\"#{2}\"/>\n\t</ClassAssertion>\n"
                        ontology.addAxiom(assertion.format(annotation, someValues, granule))

    elif rangeClassesList != [""] and auxiliaryClass != "" and objectProperty != ["", ""]:

        for inheritanceClass in rangeClassesList:
            for inheritanceClassDomain in domainClassesList:
                # Get list of centroids from centroids.csv.
                csvhandler = CSVHandler(
                    'output/' + Main._time + '/csv_files/' + auxiliaryClass + inheritanceClassDomain + inheritanceClass + "Centroids.csv")
                centroids = csvhandler.read()
                quantifierPrototypes = [float(c[0]) for c in centroids]

                # Get number of quantifierPrototypes.
                N = len(quantifierPrototypes)

                # Get granules from granules.csv.
                csvhandler = CSVHandler(
                    'output/' + Main._time + '/csv_files/' + auxiliaryClass + inheritanceClassDomain + inheritanceClass + "Granules.csv")
                granules, glabels = csvhandler.readDict()
                glabels = glabels[2:]

                # Get granules cardinalities from cardinalities.csv.
                csvhandler = CSVHandler(
                    'output/' + Main._time + '/csv_files/' + auxiliaryClass + inheritanceClassDomain + inheritanceClass + "Cardinalities.csv")
                cardinalities, _ = csvhandler.readDict()

                # Get quantifiers from quantifiers.csv.
                csvhandler = CSVHandler(
                    'output/' + Main._time + '/csv_files/' + auxiliaryClass + inheritanceClassDomain + inheritanceClass + "Quantifiers.csv")
                quantifiers, qlabels = csvhandler.readDict()
                qlabels.remove("granules")

                # Add fuzzy granules as OWL classes, where each identifier is extracted from glabels list.

                for granule in glabels:
                    ontology.addClass(trim(granule))

                # Add data property as object property.
                ontology.addObjectProperty(dataPropertyToFuzzify)
                ontology.addObjectPropertyDomain(dataPropertyToFuzzify, auxiliaryClass)

                # Add domainClass subclasses. Every subclass name is extracted from glabels list and concatenated with
                # name data property and other class of relations string.
                for granule in glabels:
                    label = trim(
                        granule) + nameProperty + auxiliaryClass + inheritanceClassDomain + "From" + inheritanceClass
                    ontology.addClass(label)
                    # Every auxiliar class subclass is defined as intersection between auxiliar class and range class
                    # and individual class obtained from existential quantifier restriction.
                    someValuesRange = ontology.objectSomeValuesFromAxiom(objectProperty[1], trim(inheritanceClass))
                    someValues = ontology.objectSomeValuesFromAxiom(dataPropertyToFuzzify, trim(granule))
                    intersectionAxiom = ontology.objectIntersectionOfAxiom(auxiliaryClass, someValuesRange + someValues)
                    ontology.addEquivalentClasses(label, intersectionAxiom)

                # Add Granule class with individuals defined as acronyms of glabels items
                listGranule = []
                dictGranule = {}
                for i in range(1, len(glabels) + 1):
                    countGranule = countGranule + 1
                    listGranule.append("granule" + str(countGranule))

                dictGranule[inheritanceClass] = listGranule
                ontology.addClass("Granule", listGranule)

                # Add left-shoulder fuzzy datatype using FuzzyOWL2 formalism.
                annotation = ("<fuzzyOwl2 fuzzyType=\"datatype\">"
                              "<Datatype type=\"leftshoulder\" a=\"{0}\" b=\"{1}\"/>"
                              "</fuzzyOwl2>").format(quantifierPrototypes[0], quantifierPrototypes[1])
                restriction = ontology.datatypeFacetRestrictionAxiom("double", "minInclusive", k1, "maxInclusive",
                                                                     k2)
                ontology.addDatatypeDefinition(trim(glabels[0]), restriction, annotation)

                # For every triangular fuzzy set, add triangular fuzzy datatype using FuzzyOWL2 formalism.
                for i in range(1, N - 1):
                    annotation = ("<fuzzyOwl2 fuzzyType=\"datatype\">"
                                  "<Datatype type=\"triangular\" a=\"{0}\" b=\"{1}\" c=\"{2}\"/>"
                                  "</fuzzyOwl2>").format(quantifierPrototypes[i - 1], quantifierPrototypes[i],
                                                         quantifierPrototypes[i + 1])
                    ontology.addDatatypeDefinition(trim(glabels[0]), restriction, annotation)

                # Add right-shoulder fuzzy datatype using FuzzyOWL2 formalism.
                annotation = ("<fuzzyOwl2 fuzzyType=\"datatype\">"
                              "<Datatype type=\"rightshoulder\" a=\"{0}\" b=\"{1}\"/>"
                              "</fuzzyOwl2>").format(quantifierPrototypes[N - 2], quantifierPrototypes[N - 1])
                ontology.addDatatypeDefinition(trim(glabels[0]), restriction, annotation)

                # Add mapsTo object property.
                ontology.addObjectProperty("mapsTo")

                # Every individual of auxiliar class is defined in relative auxialiar class subclasses and mapped with relative granules.
                # The membership degree is represented using FuzzyOWL2 code written into an annotation property.
                for row in granules:
                    i = 0
                    for granule in glabels:
                        i = i + 1
                        label = trim(
                            granule) + nameProperty + auxiliaryClass + inheritanceClassDomain + "From" + inheritanceClass
                        subClass = row.get(auxiliaryClass)
                        degree = float(row.get(granule))

                        if degree > 0:
                            annotation = "<fuzzyOwl2 fuzzyType=\"axiom\"><Degree value=\"{}\"/></fuzzyOwl2>".format(
                                degree)
                            ontology.addIndividual(subClass, label, annotation)
                            ontology.addObjectProperty("mapsTo", subClass, dictGranule.get(inheritanceClass)[i - 1])

                # Add fuzzy quantifiers as Quantifiers subclasses. Every subclass is extracted from qlabels list.
                ontology.addClass("Quantifier")
                for label in qlabels:
                    ontology.addClass(trim(label))
                    ontology.addSubClass(trim(label), "Quantifier")

                # Define hasCardinality as functional datatype property with domain class "Granule" and range in double datatype.
                ontology.addDatatypeProperty("hasCardinality")
                ontology.addDatatypePropertyDomain("hasCardinality", "Granule")
                ontology.addDatatypePropertyRange("hasCardinality", "double")
                ontology.addFunctionalDatatypeProperty("hasCardinality")

                # Add hasCardinality datatype property that put in relationship Granule's individuals with their sigma-count values.

                for row in cardinalities:
                    i = 0
                    for label in glabels:
                        i = i + 1
                        if row.get("granule") == label:
                            granule = dictGranule.get(inheritanceClass)[i - 1]
                    sigmacount = float(row.get("sigma-count"))
                    ontology.addDatatypeProperty("hasCardinality", granule, "double", Round(sigmacount))

                # Add hasCardinality object property.
                ontology.addObjectProperty("g_hasCardinality")
                ontology.addObjectPropertyDomain("g_hasCardinality", "Granule")
                ontology.addObjectPropertyRange("g_hasCardinality", "Quantifier")

                # Every granule is connected with relative quantifier class.
                for row in quantifiers:
                    for label in qlabels:
                        i = 0
                        for l in glabels:
                            i = i + 1
                            if row.get("granules") == l:
                                granule = dictGranule.get(inheritanceClass)[i - 1]
                        degree = float(row.get(label))
                        if degree > 0:
                            # The membership degree is represented using FuzzyOWL2 code written into an annotation property.
                            annotation = ontology.fuzzyLabelAnnotation(
                                "<fuzzyOwl2><Degree value=\"{}\"/></fuzzyOwl2>".format(degree))
                            # Define the existential restriction (hasCardinality some <<label>>)
                            someValues = ontology.objectSomeValuesFromAxiom("g_hasCardinality", trim(label))
                            # <<granule>> is an individual of class obtained from existential property (hasCardinality some <<label>>)
                            assertion = "\n\t<ClassAssertion>{0}{1}\n\t\t<NamedIndividual IRI=\"#{2}\"/>\n\t</ClassAssertion>\n"
                            ontology.addAxiom(assertion.format(annotation, someValues, granule))

    # Close the ontology.
    t1 = time()
    logging.warning("Time elapsed in integration process: {0:.3f} seconds.\n".format(t1 - t0))
    ontology.close()


def createNameProperty(dataPropertyToFuzzify):
    """
    Creates the name property

    :param dataPropertyToFuzzify: the data property to fuzzify
    :return: the name property
    """
    if not dataPropertyToFuzzify.islower():
        i = -1
        propertyInverse = ""
        n = len(dataPropertyToFuzzify)
        while i > -n:
            propertyInverse = propertyInverse + dataPropertyToFuzzify[i]
            if dataPropertyToFuzzify[i].isupper():
                break
            i = i - 1

        Property = ""
        i = -1
        n = len(propertyInverse)
        while i >= -n:
            Property = Property + propertyInverse[i]
            i = i - 1

        return Property
    else:
        return dataPropertyToFuzzify


def getIndividualsClass(SPARQLEndpoint, ontologyPrefix, domainClass):
    """
    Gets the numbers of individuals of the specified class

    :param SPARQLEndpoint: the sparql endpoint
    :param ontologyPrefix: the query prefix
    :param domainClass: the domain class
    :return: the length of the resultset
    """
    # obtain a connection to the endpoint
    sparql = SPARQLEndpointInterface(SPARQLEndpoint)

    query = ("PREFIX ontology: " + ontologyPrefix +
             " SELECT ?individual  WHERE {"
             "  ?individual a ontology:" + domainClass + ".  } ")

    # sends the query
    rs, fields = ResultSetConverter.convertToLD(sparql(query))

    # store only the identifiers of generic class
    resultset = [row.get("individual").split("#", 1)[1] for row in rs]
    return len(resultset)


def createOutputAndLogFiles():
    """
    Create output folder and starts the debug.log file
    """
    Main._time = datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S")

    if not os.path.exists('output/' + Main._time):
        os.makedirs('output/' + Main._time)

    logging.basicConfig(filename='output/' + Main._time + '/debug.log',
                        level=logging.DEBUG, format='%(message)s')


def renameOutputFolder():
    """
    Renames the output folder appending '_FAILED' string
    """
    logging.shutdown()
    shutil.move('output/' + Main._time, 'output/' + Main._time + '_FAILED')


def increaseLabels(fuzzySetLabels):
    """
    Increases the counter of fuzzy set label to not incur in a puning error in the integrated ontology

    :param fuzzySetLabels: the fuzzy set labels list
    :return: the new countered increased fuzzy set labels list
    """
    newFuzzySetLabels = []

    for label in fuzzySetLabels:
        newFuzzySetLabels.append(label + str(Main._index))
    Main._index += 1

    return newFuzzySetLabels


def pruning(SPARQLEndpoint, ontologyPrefix, classesList, fuzzySetLabelsLength):
    for c in classesList:
        if getIndividualsClass(SPARQLEndpoint, ontologyPrefix, c) <= fuzzySetLabelsLength:
            logging.warning("Instance of '" + c + "' are not sufficient!")
            classesList.remove(c)
    return classesList


def execute_operations(ontologyName, SPARQLEndPoint, ontologyPrefix, dataPropertyToFuzzify, fuzzySetLabels,
                       quantifierLabels, quantifierPrototypes, domainClasses,
                       rangeClasses=[""], auxiliaryClass="",
                       objectProperty=[""]):
    """
    Executes all the operations for all the combinations between domain classes list and range classes list. These
    operations are:

    - query execution to retrieve data from the ontology
    - fuzzy clustering on data
    - granulation on data
    - quantification on data
    - integration of results on the original ontology

    :param ontologyName: the ontology name
    :param SPARQLEndPoint: the sparql endpoint SPARQLEndpoint
    :param ontologyPrefix: the ontology prefix for the queries
    :param dataPropertyToFuzzify: the data property to fuzzify
    :param fuzzySetLabels: the fuzzy set labels list
    :param quantifierLabels: the quantifier labels list
    :param quantifierPrototypes: the quantifier prototypes
    :param domainClasses: the domain classes list
    :param rangeClasses: the range classes list (if empty, the operations are binary)
    :param auxiliaryClass: the auxiliary class (if empty, the operations are binary)
    :param objectProperty: the object property (if empty, the operations are binary)
    """
    pruning(SPARQLEndPoint, ontologyPrefix, domainClasses, len(fuzzySetLabels))
    for domain in domainClasses:
        for range in rangeClasses:
            labels = increaseLabels(fuzzySetLabels)
            executeQuery(SPARQLEndPoint, ontologyPrefix, dataPropertyToFuzzify, domain, range, auxiliaryClass,
                         objectProperty)
            clustering(len(fuzzySetLabels), dataPropertyToFuzzify, domain, range, auxiliaryClass)
            granulation(labels, dataPropertyToFuzzify, domain, range, auxiliaryClass)
            quantification(quantifierLabels, quantifierPrototypes, dataPropertyToFuzzify, domain, range,
                           auxiliaryClass)
    integration(ontologyName, dataPropertyToFuzzify, domainClasses, rangeClasses, auxiliaryClass,
                objectProperty)


def main():
    try:
        t0 = time()
        createOutputAndLogFiles()
        logging.warning("PROCESS STARTED...\n")

        data = json.loads(open('config.json').read())
        consistencycheck = ConsistencyCheck(data)

        if consistencycheck():
            execute_operations(data["ontologyName"], data["SPARQLEndPoint"], data["ontologyPrefix"],
                               data["dataPropertyToFuzzify"], data["fuzzySetsLabels"], data["quantifiersLabels"],
                               data["quantifiersPrototypes"], data["domainClasses"], data["rangeClasses"],
                               data["auxiliaryClass"], [data["objectPropertyToAuxiliaryClass"],
                                                        data["objectPropertyFromAuxiliaryClass"]])
            logging.warning("\nTHE WHOLE PROCESS WAS PERFORMED IN {0:.3f} SECONDS.".format(time() - t0))
        else:
            # If something is wrong with the configuration file, the output folder is renamed appending '_FAILED' string
            # and the error print in debug.log
            print("PROCESS STOPPED DUE TO AN ERROR: check debug.log for more informations")
            logging.warning("\nPROCESS STOPPED DUE TO AN ERROR")
            renameOutputFolder()

    except Exception:
        # If an exception is raised during the process, the output folder is renamed appending '_FAILED' string
        renameOutputFolder()
        raise Exception


if __name__ == '__main__':
    main()
