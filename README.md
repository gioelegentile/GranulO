# **GranulO**    ![logo](https://www.gnu.org/graphics/gplv3-88x31.png)

GranulO is an application for the fuzzy granulation of some schemas in OWL ontologies.

For further information on the method, see:
Lisi, Francesca A., and Corrado Mencar. "Towards fuzzy granulation in OWL ontologies." *Proceedings of the 30th Italian Conference on Computational Logic*, Genova, Italy. 2015.
(Available at [http://ceur-ws.org/Vol-1459/paper19.pdf](Link URL))

Version 1.0, GNU General Public License v3.0.

## **How to use** ##

- Install [Apache Jena Fuseki 2](https://jena.apache.org/index.html). 
- Modify the content of the `fuseki-server.bat` file with the following text, in order to assign more RAM to Jena and to start it with the custom configuration file: 

```
#!batch

java -Xmx3500M -jar fuseki-server.jar --config=config.ttl
``` 

- The content of the `config.ttl` file is the following. It will activate the OWL reasoner:

```
#!rdf

# Licensed under the terms of http://www.apache.org/licenses/LICENSE-2.0

@prefix : <#> .
@prefix fuseki: <http://jena.apache.org/fuseki#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix tdb: <http://jena.hpl.hp.com/2008/tdb#> .
@prefix ja: <http://jena.hpl.hp.com/2005/11/Assembler#> .

[] rdf:type fuseki:Server ;
	fuseki:services (
		<#service1>
	) 
.
 
[] ja:loadClass "com.hp.hpl.jena.tdb.TDB" .

tdb:DatasetTDB rdfs:subClassOf ja:RDFDataset .
tdb:GraphTDB rdfs:subClassOf ja:Model .

<#service1> 
	rdf:type fuseki:Service ;
	fuseki:name "inf" ; # http://host/inf
	fuseki:serviceQuery "sparql" ; # SPARQL query service
	fuseki:serviceUpdate "update" ;
	fuseki:serviceUpload "upload" ; # Non-SPARQL upload service
	fuseki:serviceReadWriteGraphStore "data" ;
	# A separate read-only graph store endpoint
	fuseki:serviceReadGraphStore "get" ;
	fuseki:dataset <#dataset> ;
	
.
	
<#dataset> 
	rdf:type ja:RDFDataset ;
	ja:defaultGraph <#model_inf> ;
.

<#model_inf> 
	a ja:InfModel ;
	ja:baseModel <#tdbGraph> ;
	ja:reasoner [
		ja:reasonerURL <http://jena.hpl.hp.com/2003/OWLFBRuleReasoner>
	]
.
 
<#tdbDataset> 
	rdf:type tdb:DatasetTDB ;
	tdb:location "DB" ;
	# If the unionDefaultGraph is used, then the "update" service should be removed.
	# The unionDefaultGraph is read only.
	# tdb:unionDefaultGraph true ;
.

<#tdbGraph> 
	rdf:type tdb:GraphTDB ;
	tdb:dataset <#tdbDataset> 
.
```

* Access Jena interface from http://localhost:3030.
* Create a dataset and upload the ontologies you want in RDF/XML syntax.

## ***JSON* configuration file** ##

In the JSON configuration file there are parameters useful to the execution of the process.
The content of the `config.json` file is the following:

```
#!json
{
    "ontologyName" : "ontology.owl",
    "ontologyPrefix" : "<http://www.semanticweb.org/ontologies/ontology.owl#>",
    "SPARQLEndPoint" : "http://localhost:3030/dataset/sparql",

    "domainClasses" : ["domain1", "domain2"],
    "rangeClasses" : [""],

    "objectPropertyToAuxiliaryClass" : "",
    "auxiliaryClass" : "",
    "objectPropertyFromAuxiliaryClass" : "",

    "dataPropertyToFuzzify" : "hasValue",
    "fuzzySetsLabels" : ["Low", "Mid", "High"],

    "quantifiersLabels" : ["AlmostNone", "Few", "Some", "Many", "Most"],
    "quantifiersPrototypes" : [0.05, 0.275, 0.5, 0.725, 0.95]
}

```
You can run GranulO on OWL schemas which represent binary or ternary relations. If you want to test GranulO on a ternary relation, you simply have to fill the blank parameters. Otherwise, the process will be executed by considering the relation as binary. There are no other possible configurations.

## **Notes** ##

- The python application only accept ontologies in OWL/XML syntax. Jena needs ontologies in RDF/XML syntax instead. So you will need two versions of the same ontology.
