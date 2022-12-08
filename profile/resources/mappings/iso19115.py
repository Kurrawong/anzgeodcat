"""
ANZGeoDCAT Profile Resource

This Python script converts ANZGeoDCAT (https://linked.data.gov.au/def/anzgeodcat) RDF data to XML data conforming
to the Geoscience Australia Profile of ISO19115-1 (http://pid.geoscience.gov.au/dataset/ga/122551) and vice versa.

USE
This script only operates as a command line arguments Python script.

Running the help command, -h, will reveal all options:

~$ python iso19115.py -h


INSTALLATION
To run this script you need the following installed:

* Python (3.6+)
* rdflib - Python module for RDF data manipulation
* lxml - Python module for XML manipulation
"""
from rdflib import Graph


