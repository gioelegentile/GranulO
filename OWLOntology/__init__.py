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
import sys
from html import escape

from utils import FileHandler


class OWLOntology(object):
    '''
    This class occupies to insert additional axiom in the OWL ontology using
    OWL/XML syntax. It requires an ontology written in OWL/XML syntax.
    Every modifies are added into a backup ontology in order to keep original
    version of the given ontology.
    
    '''

    def __init__(self, filename):
        '''
        Initializes the instances of the class.
        
        :Parameter:
        ontology: filename of the ontology
        
        '''
        self.addedindividualsCount = 0
        self.addedclassesCount = 0
        self.addedaxiomsCount = 0
        self.addedassertionsCount = 0
        self._ontologyClosureTag = "</Ontology>\n"
        self._ontology = FileHandler(filename)
        self._append_string = ""
        if not self._ontology.exists():
            raise Exception("[OWLOntology] ERROR: {} file does not exists.".format(filename))

    def close(self):
        '''
        This function finalizes the ontology backup.
        
        '''
        self.printcounts()
        if self._backup and self._append_string:
            print(sys.getsizeof(self._append_string))
            self._backup.append(self._append_string)
            self._backup.append(self._ontologyClosureTag)
            self._ontology = self._backup
            self._backup = None

    def append_string(self, string):
        if sys.getsizeof(self._append_string) < 1000000:
            self._append_string += string
        else:
            self._backup.append(self._append_string)
            self._backup.append(string)
            self._append_string = ""

    def printcounts(self):
        logging.warning("METRICS:")
        logging.warning("The process added " + str(self.addedindividualsCount) + " individuals to the ontology.")
        logging.warning("The process added " + str(self.addedclassesCount) + " classes to the ontology.")
        logging.warning("The process added " + str(self.addedaxiomsCount) + " axioms to the ontology.")
        logging.warning("The process added " + str(self.addedassertionsCount) + " assertions to the ontology.")

    def createBackup(self, filename):
        '''
        This function create a backup of the current ontology, there new axioms
        will be written.
        
        :Parameters:
        filename: filename of the backup file.
        
        :Returns:
        self._backup: instance of FileHandler
        
        '''
        self._backup = FileHandler(filename)
        ontology = self._ontology.readAll()
        index = len(ontology) - 1
        while ontology[index] != self._ontologyClosureTag:
            index = index - 1
        del ontology[index]
        self._backup.writeAll(ontology)
        return self._backup

    def fuzzyLabelAnnotation(self, fuzzyowl):
        '''
        
        :Parameters:
        fuzzyowl: .
        
        :Returns:
        annotation: annotation property in string form.
        '''
        annotation = (
            "\n\t\t<Annotation>"
            "\n\t\t\t<AnnotationProperty IRI=\"#fuzzyLabel\"/>"
            "\n\t\t\t<Literal datatypeIRI=\"&rdf;PlainLiteral\">{}</Literal>"
            "\n\t\t</Annotation>").format(escape(fuzzyowl, quote=True))
        return annotation

    def addAxiom(self, axiom):
        '''
        This function adds a general axiom expressed in OWL/XML syntax.
        
        :Parameters:
        axiom: the axiom in string format.
        '''
        self.addedaxiomsCount += 1
        self.append_string(axiom)

    def addIndividual(self, individual, classId=None, annotation=""):
        '''
        This function adds a single individual into the ontology.
        
        :Parameters:
        individual: identifier of the individual.
        classId: identifier of the class where the individual is an instance.
        
        '''
        axiom = ""
        if annotation:
            annotation = self.fuzzyLabelAnnotation(annotation)
        if classId:
            axiom = (
                "\n\t<ClassAssertion>"
                "{0}"
                "\n\t\t<Class IRI=\"#{1}\"/>"
                "\n\t\t<NamedIndividual IRI=\"#{2}\"/>"
                "\n\t</ClassAssertion>\n").format(annotation, classId, individual)
        else:
            axiom = (
                "\n\t<Declaration>"
                "{0}"
                "\n\t\t<NamedIndividual IRI=\"{1}\"/>"
                "\n\t</Declaration>\t").format(annotation, individual)
        self.addedindividualsCount += 1
        self.addedassertionsCount += 1
        self.append_string(axiom)

    def addDifferentIndividuals(self, first, second):
        '''
        This function adds an axiom that states two individuals are different.
        
        :Parameters:
        first: identifier of first individual
        second: identifier of second individual
        
        '''
        different = (
            "\n\t<DifferentIndividuals>"
            "\n\t\t<NamedIndividual IRI=\"#{0}\"/>"
            "\n\t\t<NamedIndividual IRI=\"#{1}\"/>"
            "\n\t</DifferentIndividuals>\n").format(first, second)
        self.addedassertionsCount += 1
        self.append_string(different)

    def addClass(self, className, individuals=None, annotation=""):
        '''
        This function adds a new class into the ontology. If individuals
        parameter is set to None, a declaration of the class without
        individuals will be added.
        
        :Parameters:
        className: identifier of the new class.
        individuals: list of identifiers of class individuals.
        annotation: annotation assertion to apply at this axiom.
        
        '''
        if annotation:
            annotation = self.fuzzyLabelAnnotation(annotation)
        declaration = (
            "\n\t<Declaration>"
            "{0}"
            "\n\t\t<Class IRI=\"#{1}\"/>"
            "\n\t</Declaration>\n").format(annotation, className)
        self.addedaxiomsCount += 1
        self.addedclassesCount += 1
        self.append_string(declaration)
        if individuals:
            for individual in individuals:
                self.addIndividual(individual, className)

    def classAxiom(self, classId):
        '''
        This function defines a class axiom.
        
        :Parameters:
        classId: identifier of the class.
        
        :Return:
        the class axiom in string form.
        '''
        return "<Class IRI=\"#{}\"/>".format(classId)

    def addSubClass(self, subClass, superClass):
        '''
        This function creates a sub class of an existent class of the ontology.
        
        :Parameters:
        subClass: identifier of the sub class.
        superClass: identifier of the super class
        
        '''
        subclassaxiom = (
            "\n\t<SubClassOf>"
            "\n\t\t<Class IRI=\"#{0}\"/>"
            "\n\t\t<Class IRI=\"#{1}\"/>"
            "\n\t</SubClassOf>\n").format(subClass, superClass)
        self.addedaxiomsCount += 1
        self.append_string(subclassaxiom)

    def addDisjointClasses(self, first, second):
        '''
        This function adds an axiom which define two disjoint classes.
        
        :Parameters:
        first: identifier of a disjoint class.
        second: identifier of a disjoint class.
        
        '''
        disjoint = (
            "\n\t<DisjointClasses>"
            "\n\t\t<Class IRI=\"#{0}\"/>"
            "\n\t\t<Class IRI\"#{1}\"/>"
            "\n\t</DisjointClasses>\n").format(first, second)
        self.addedaxiomsCount += 1
        self.append_string(disjoint)

    def addObjectProperty(self, objProperty, first=None, second=None):
        '''
        This function adds an object property between two classes. If first and
        second parameters are set to None, a declaration axiom of property will
        be added. 
        
        :Parameters:
        first: identifier of the domain class.
        second: identifier of the range class.
        
        '''
        objectProperty = ""
        if first and second:
            objectProperty = (
                "\n\t<ObjectPropertyAssertion>"
                "\n\t\t<ObjectProperty IRI=\"#{0}\"/>"
                "\n\t\t<NamedIndividual IRI=\"#{1}\"/>"
                "\n\t\t<NamedIndividual IRI=\"#{2}\"/>"
                "\n\t</ObjectPropertyAssertion>\n").format(objProperty, first, second)
        else:
            objectProperty = (
                "\n\t<Declaration>"
                "\n\t\t<ObjectProperty IRI=\"#{}\"/>"
                "\n\t</Declaration>\n").format(objProperty)
        self.addedassertionsCount += 1
        self.append_string(objectProperty)

    def addFunctionalObjectProperty(self, objProperty):
        '''
        This function adds an axiom that states a object property is functional.
        
        :Parameters:
        objProperty: identifier of object property.
        '''
        functionalProperty = (
            "\n\t<FunctionalObjectProperty>"
            "\n\t\t<ObjectProperty IRI=\"#{}\"/>"
            "\n\t</FunctionalObjectProperty>\n").format(objProperty)
        self.append_string(functionalProperty)

    def addObjectPropertyDomain(self, objProperty, domainClass):
        propertyRestriction = (
            "\n\t<ObjectPropertyDomain>"
            "\n\t\t<ObjectProperty IRI=\"#{0}\"/>"
            "\n\t\t<Class IRI=\"#{1}\"/>"
            "\n\t</ObjectPropertyDomain>").format(objProperty, domainClass)
        self.append_string(propertyRestriction)

    def addObjectPropertyRange(self, objProperty, rangeClass):
        '''
        This function adds a property domain and range restriction to an object
        property.
        
        :Parameters:
        objProperty: identifier of the object property.
        domainClass: identifier of the domain class.
        rangeClass: identifier of the range class.
        
        '''
        propertyRestriction = (
            "\n\t<ObjectPropertyDomain>"
            "\n\t\t<ObjectProperty IRI=\"#{0}\"/>"
            "\n\t\t<Class IRI=\"#{1}\"/>"
            "\n\t</ObjectPropertyDomain>").format(objProperty, rangeClass)
        self.append_string(propertyRestriction)

    def addDatatypeProperty(self, dataProperty, individual=None, datatype=None, value=None):
        '''
        This class adds a datatype property between individuals and datatypes.
        If individual, datatype and value parameters are set to None,
        a declaration axiom of property will be added.
        
        :Parameters:
        dataProperty: identifier of the datatype property.
        individual: indentifier of the individual.
        datatype: identifier of the datatype.
        value: datatype value.
        
        '''
        datatypeProperty = ""
        if individual and datatype and value:
            datatypeProperty = (
                "\n\t<DataPropertyAssertion>"
                "\n\t\t<DataProperty IRI=\"#{0}\"/>"
                "\n\t\t<NamedIndividual IRI=\"#{1}\"/>"
                "\n\t\t<Literal datatypeIRI=\"&xsd;{2}\">{3}</Literal>"
                "\n\t</DataPropertyAssertion>\n").format(dataProperty, individual, datatype, value)
        else:
            datatypeProperty = (
                "\n\t<Declaration>"
                "\n\t\t<DataProperty IRI=\"#{}\"/>"
                "\n\t</Declaration>\n").format(dataProperty)
        self.addedassertionsCount += 1
        self.append_string(datatypeProperty)

    def addFunctionalDatatypeProperty(self, dataProperty):
        '''
        This function adds an axiom that states a datatype property is functional.
        
        :Parameters:
        dataProperty: identifier of datatype property.
        '''
        functionalProperty = (
            "\n\t<FunctionalDataProperty>"
            "\n\t\t<DataProperty IRI=\"#{}\"/>"
            "\n\t</FunctionalDataProperty>\n").format(dataProperty)
        self.append_string(functionalProperty)

    def addDatatypePropertyDomain(self, dataProperty, domainClass):
        '''
        This function adds a property domain restriction to datatype property.
        
        :Parameter:
        dataProperty: identifier of the datatype property.
        domainClass: identifier of the domain class.
        
        '''
        propertyRestriction = (
            "\n\t<DataPropertyDomain>"
            "\n\t\t<DataProperty IRI=\"#{0}\"/>"
            "\n\t\t<Class IRI=\"#{1}\"/>"
            "\n\t</DataPropertyDomain>"
        ).format(dataProperty, domainClass)
        self.append_string(propertyRestriction)

    def addDatatypePropertyRange(self, dataProperty, datatype="", facetRestriction=""):
        '''
        This function adds a property range restriction to datatype property.
        
        :Parameter:
        dataProperty: identifier of the datatype property.
        datatype: identifier of datatype.
        
        '''
        if datatype:
            axiom = "\n\t\t<Datatype IRI=\"&xsd;{}\"/>".format(datatype)
        elif facetRestriction:
            axiom = facetRestriction
        propertyRestriction = (
            "\n\t<DataPropertyRange>"
            "\n\t\t<DataProperty IRI=\"#{0}\"/>"
            "{1}"
            "\n\t</DataPropertyRange>\n").format(dataProperty, axiom)
        self.append_string(propertyRestriction)

    def addDatatypeDefinition(self, dataDefinition, facetRestriction, annotation=""):
        '''
        This functions add a datatype definition in order to create a new
        datatype to represent a range of data.
        
        :Parameters:
        dataDefinition: identifier of new datatype to define.
        datatype: identifier of datatype used to represent the dataset.
        facetRestriction: maximum value of dataset.
        annotation: annotation in string format.
        
        '''
        if annotation:
            annotation = self.fuzzyLabelAnnotation(annotation)
        definition = (
            "\n\t<DatatypeDefinition>"
            "{0}"
            "\n\t\t<Datatype IRI=\"#{1}\"/>"
            "{2}"
            "\n\t</DatatypeDefinition>\n").format(annotation, dataDefinition, facetRestriction)
        self.append_string(definition)

    def datatypeFacetRestrictionAxiom(self, datatype, firstFacet, firstValue, secondFacet, secondValue):
        '''
        This function adds a facet restriction to a datatype in order to
        define a range of allowed values. 
        
        :Parameters:
        datatype: identifier of datatype.
        firstFacet: identifier of first facet restriction.
        firstValue: first literal datatype value.
        secondFacet: identifier of second facet restriction.
        secondValue: second literal datatype value.
        
        :Return:
        facet restriction in string format.
        
        '''
        facetRestriction = (
            "\n\t\t<DatatypeRestriction>"
            "\n\t\t\t<Datatype IRI=\"&xsd;{0}\"/>"
            "\n\t\t\t<FacetRestriction facet=\"&xsd;{1}\">"
            "\n\t\t\t\t<Literal datatypeIRI=\"&xsd;{0}\">{2}</Literal>"
            "\n\t\t\t</FacetRestriction>"
            "\n\t\t\t<FacetRestriction facet=\"&xsd;{3}\">"
            "\n\t\t\t\t<Literal datatypeIRI=\"&xsd;{0}\">{4}</Literal>"
            "\n\t\t\t</FacetRestriction>"
            "\n\t\t</DatatypeRestriction>").format(datatype, firstFacet, firstValue, secondFacet, secondValue)
        return facetRestriction

    def addEquivalentClasses(self, classId, axiom):
        '''
        This function adds an equivalent classes assertion into the ontology.
        
        :Parameters:
        classId: identifier of the class.
        axiom: sub axiom of an equivalent class.
        
        '''
        equivalent = (
            "\n\t<EquivalentClasses>"
            "\n\t\t<Class IRI=\"#{0}\"/>"
            "{1}"
            "\n\t</EquivalentClasses>\n").format(classId, axiom)
        self.addedaxiomsCount += 1
        self.append_string(equivalent)

    def objectHasValue(self, objProperty, individual):
        '''
        This function defines an object property value.
        
        :Parameters:
        objProperty: identifier of the object property.
        individual: identifier of the individual.
        
        :Returns:
        hasValue: ObjectHasValue axiom in string form.
        '''
        hasValue = (
            "\n\t\t<ObjectHasValue>"
            "\n\t\t\t<ObjectProperty IRI=\"#{0}\"/>"
            "\n\t\t\t<NamedIndividual IRI=\"#{1}\"/>"
            "\n\t\t</ObjectHasValue>\n").format(objProperty, individual)
        return hasValue

    def objectSomeValuesFromAxiom(self, objProperty, className):
        '''
        This function define an existential quantification for an object property.
        
        :Parameters:
        objProperty: identifier of object property.
        className: identifier of the class.
        
        :Returns:
        someValues: existential quantification axiom in string form.
        
        '''
        someValues = (
            "\n\t\t\t<ObjectSomeValuesFrom>"
            "\n\t\t\t\t<ObjectProperty IRI=\"#{0}\"/>"
            "\n\t\t\t\t<Class IRI=\"#{1}\"/>"
            "\n\t\t\t</ObjectSomeValuesFrom>\n").format(objProperty, className)
        return someValues

    def addObjectSomeValueFrom(self, objProperty, domainClass, rangeClass):
        '''
        This function adds an existential quantification for an object property.
        
        :Parameters:
        objProperty: identifier of object property.
        domainClass: identifier of domain class.
        rangeClass: identifier of range class.
        
        '''
        someValuesAxiom = self.objectSomeValuesFromAxiom(objProperty, rangeClass)
        self.addedassertionsCount += 1
        self.addEquivalentClasses(domainClass, someValuesAxiom)

    def objectAllValuesFromAxiom(self, objProperty, className):
        '''
        This function define an universal quantification for an object property.
        
        :Parameters:
        objProperty: identifier of object property.
        className: identifier of the class.
        
        :Returns:
        allValues: universal quantification axiom in string form.
        '''
        allValues = (
            "\n\t\t<ObjectAllValuesFrom>"
            "\n\t\t\t<ObjectProperty IRI=\"#{0}\"/>"
            "\n\t\t\t<Class IRI=\"#{1}\"/>"
            "\n\t\t</ObjectAllValuesFrom>\n").format(objProperty, className)
        return allValues

    def addObjectAllValuesFrom(self, objProperty, domainClass, rangeClass):
        '''
        This function adds an universal quantification for an object property.
        
        :Parameters:
        objProperty: identifier of object property.
        domainClass: identifier of domain class.
        rangeClass: identifier of range class.
        
        '''
        allValuesAxiom = self.objectAllValuesFromAxiom(objProperty, rangeClass)
        self.addEquivalentClasses(domainClass, allValuesAxiom)

    def objectUnionOfAxiom(self, classId, axiom):
        '''
        This function defines an union axiom.
        
        :Parameters:
        classId: identifier of a class.
        axiom: sub axiom of union axiom.
        
        :Returns:
        union axiom in string form.
        
        '''
        union = (
            "\n\t\t<ObjectUnionOf>"
            "\n\t\t\t<Class IRI=\"#{0}\"/>"
            "\n\t\t\t{1}"
            "\n\t\t</ObjectUnionOf>\n").format(classId, axiom)
        return union

    def addObjectUnionOf(self, mainClass, first, second):
        '''
        This function adds an axiom that specifies the equivalence of a class
        with the union of two several classes.
        
        :Parameters:
        mainClass: identifier of the result class.
        first: identifier of a class.
        second: identifier of a class.
        
        '''
        s = self.classAxiom(second)
        union = self.objectUnionOfAxiom(first, s)
        self.addEquivalentClasses(mainClass, union)

    def objectIntersectionOfAxiom(self, classId, axiom):
        '''
        This function defines an intersection axiom.
        
        :Parameters:
        classId: identifier of the class.
        axiom: sub axiom to insert.
        
        :Returns:
        intersection axiom in string form.
        
        '''
        intersection = (
            "\n\t\t<ObjectIntersectionOf>"
            "\n\t\t\t<Class IRI=\"#{0}\"/>"
            "\n\t\t\t{1}"
            "\n\t\t</ObjectIntersectionOf>\n").format(classId, axiom)
        return intersection

    def addObjectIntersectionOf(self, mainClass, first, second):
        '''
        This function adds an axiom that specifies the equivalence of a class
        with the intersection of two several classes.
        
        :Parameters:
        mainClass: identifier of the result class.
        first: identifier of a class.
        second: identifier of a class.
        
        '''
        f = self.classAxiom(first)
        s = self.classAxiom(second)
        intersection = self.objectIntersectionOfAxiom(f, s)
        self.addEquivalentClasses(mainClass, intersection)

    def objectComplementOfAxiom(self, axiom):
        '''
        This function defines an complement axiom.
        
        :Parameters:
        axiom: sub axiom to insert.
        
        :Returns:
        complement axiom in string form.
        
        '''
        complement = (
            "\n\t\t<ObjectComplementOf>"
            "\n\t\t\t{}>"
            "\n\t\t</ObjectUnionOf>\n").format(axiom)
        return complement

    def addObjectComplementOf(self, mainClass, classId):
        '''
        This function adds an axiom that specifies the equivalence of a class
        with the complement of a given class.
        
        :Parameters:
        mainClass: identifier of the result class.
        classId: identifier of a class.
        
        '''
        axiom = self.classAxiom(classId)
        complement = self.objectComplementOfAxiom(axiom)
        self.addEquivalentClass(mainClass, complement)
