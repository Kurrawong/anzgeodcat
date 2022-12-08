__version__ = "0.1.0"
"""
An ANZGeoDCAT Profile Resource

This Python script converts ANZGeoDCAT (https://linked.data.gov.au/def/anzgeodcat) RDF data to XML data conforming
to the Geoscience Australia Profile of ISO19115-1 (http://pid.geoscience.gov.au/dataset/ga/122551) and vice versa.

(c) Intergovernmental Committee on Surveying & Mapping, 2022

See this script's code repository for more information: https://github.com/Kurrawong/anzgeodcat.


USE
This script only operates as a command line arguments Python script.

Running the help command, -h, will reveal all options:

~$ python iso19115.py -h

usage: iso19115.py [-h] [-v] [-o OUTPUTFILE] [-f OUTPUTFORMAT] [-l | --log | --no-log] input

positional arguments:
  input                 Input file path

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -o OUTPUTFILE, --outputfile OUTPUTFILE
                        An output file path. If given, output will be written to this file. If not, output will be 
                        returned
  -f OUTPUTFORMAT, --outputformat OUTPUTFORMAT
                        If converting XML to RDF, an RDF file format may be specified. Must be one of ttl, nt, jsonld, 
                        n3, rdf. Default is ttl.
  -l, --log, --no-log   If set, will print logging. If output_file is given, logging will be to std out, else to file 
                        processing.log


INSTALLATION
To run this script you need the following installed:

* Python (3.6+)
* rdflib - Python module for RDF data manipulation
* lxml - Python module for XML manipulation
"""
import argparse
from pathlib import Path
from datetime import datetime
from rdflib import Graph, URIRef, Literal, BNode, Namespace
from rdflib.namespace import DCAT, DCTERMS, OWL, RDF, RDFS, SKOS, XSD
from lxml import etree


RDF_FILE_TYPES = ["ttl", "nt", "jsonld", "n3", "rdf"]
LOGGING = "file"


def log(message: str):
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
    if LOGGING == "file":
        with open("processing.log", "a") as f:
            f.write(now + "\t" + message + "\n")
    elif LOGGING == "stdout":
        print(now + "\t" + message)
    else:
        pass


def make_xml_identifier(title, code, code_space):
    """Makes an XML identifier from given values"""
    """
      <mcc:MD_Identifier>
         <mcc:authority>
            <cit:CI_Citation>
               <cit:title>
                  <gco:CharacterString>GeoNetwork UUID</gco:CharacterString>
               </cit:title>
            </cit:CI_Citation>
         </mcc:authority>
         <mcc:code>
            <gco:CharacterString>4fce6238-8d55-499c-bff5-98518552f4b4</gco:CharacterString>
         </mcc:code>
         <mcc:codeSpace>
            <gco:CharacterString>urn:uuid</gco:CharacterString>
         </mcc:codeSpace>
      </mcc:MD_Identifier>
    """
    mcc_md_identifier = etree.Element("{http://standards.iso.org/iso/19115/-3/mcc/1.0}MD_Identifier")
    mcc_authority = etree.Element("{http://standards.iso.org/iso/19115/-3/mcc/1.0}authority")
    cit_ci_citation = etree.Element("{http://standards.iso.org/iso/19115/-3/cit/1.0}CI_Citation")
    cit_title = etree.Element("{http://standards.iso.org/iso/19115/-3/cit/1.0}title")
    gco_character_string = etree.Element("{http://standards.iso.org/iso/19115/-3/gco/1.0}CharacterString")
    mcc_code = etree.Element("{http://standards.iso.org/iso/19115/-3/mcc/1.0}code")
    gco_character_string2 = etree.Element("{http://standards.iso.org/iso/19115/-3/gco/1.0}CharacterString")
    mcc_code_space = etree.Element("{http://standards.iso.org/iso/19115/-3/mcc/1.0}codeSpace")
    gco_character_string3 = etree.Element("{http://standards.iso.org/iso/19115/-3/gco/1.0}CharacterString")

    mcc_md_identifier.append(mcc_authority)
    mcc_authority.append(cit_ci_citation)
    cit_ci_citation.append(cit_title)
    cit_title.append(gco_character_string)
    gco_character_string.text = title

    mcc_md_identifier.append(mcc_code)
    mcc_code.append(gco_character_string2)
    gco_character_string2.text = code

    mcc_md_identifier.append(mcc_code_space)
    mcc_code_space.append(gco_character_string3)
    gco_character_string3.text = code_space

    return mcc_md_identifier


def make_xml():
    """Makes XML from RDF input"""
    mdb_md_metadata = etree.Element(
        "{http://standards.iso.org/iso/19115/-3/mdb/1.0}MD_Metadata",
        attrib={
            etree.QName("http://www.w3.org/2001/XMLSchema-instance", "schemaLocation"):
                "http://standards.iso.org/iso/19115/-3/cat/1.0 "
                "http://standards.iso.org/iso/19115/-3/cat/1.0/cat.xsd "
                "http://standards.iso.org/iso/19115/-3/cit/1.0 "
                "http://standards.iso.org/iso/19115/-3/cit/1.0/cit.xsd "
                "http://standards.iso.org/iso/19115/-3/gcx/1.0 "
                "http://standards.iso.org/iso/19115/-3/gcx/1.0/gcx.xsd "
                "http://standards.iso.org/iso/19115/-3/gex/1.0 "
                "http://standards.iso.org/iso/19115/-3/gex/1.0/gex.xsd "
                "http://standards.iso.org/iso/19115/-3/lan/1.0 "
                "http://standards.iso.org/iso/19115/-3/lan/1.0/lan.xsd "
                "http://standards.iso.org/iso/19115/-3/srv/2.0 "
                "http://standards.iso.org/iso/19115/-3/srv/2.0/srv.xsd "
                "http://standards.iso.org/iso/19115/-3/mas/1.0 "
                "http://standards.iso.org/iso/19115/-3/mas/1.0/mas.xsd "
                "http://standards.iso.org/iso/19115/-3/mcc/1.0 "
                "http://standards.iso.org/iso/19115/-3/mcc/1.0/mcc.xsd "
                "http://standards.iso.org/iso/19115/-3/mco/1.0 "
                "http://standards.iso.org/iso/19115/-3/mco/1.0/mco.xsd "
                "http://standards.iso.org/iso/19115/-3/mda/1.0 "
                "http://standards.iso.org/iso/19115/-3/mda/1.0/mda.xsd "
                "http://standards.iso.org/iso/19115/-3/mdb/1.0 "
                "http://standards.iso.org/iso/19115/-3/mdb/1.0/mdb.xsd "
                "http://standards.iso.org/iso/19115/-3/mds/1.0 "
                "http://standards.iso.org/iso/19115/-3/mds/1.0/mds.xsd "
                "http://standards.iso.org/iso/19115/-3/mdt/1.0 "
                "http://standards.iso.org/iso/19115/-3/mdt/1.0/mdt.xsd "
                "http://standards.iso.org/iso/19115/-3/mex/1.0 "
                "http://standards.iso.org/iso/19115/-3/mex/1.0/mex.xsd "
                "http://standards.iso.org/iso/19115/-3/mmi/1.0 "
                "http://standards.iso.org/iso/19115/-3/mmi/1.0/mmi.xsd "
                "http://standards.iso.org/iso/19115/-3/mpc/1.0 "
                "http://standards.iso.org/iso/19115/-3/mpc/1.0/mpc.xsd "
                "http://standards.iso.org/iso/19115/-3/mrc/1.0 "
                "http://standards.iso.org/iso/19115/-3/mrc/1.0/mrc.xsd "
                "http://standards.iso.org/iso/19115/-3/mrd/1.0 "
                "http://standards.iso.org/iso/19115/-3/mrd/1.0/mrd.xsd "
                "http://standards.iso.org/iso/19115/-3/mri/1.0 "
                "http://standards.iso.org/iso/19115/-3/mri/1.0/mri.xsd "
                "http://standards.iso.org/iso/19115/-3/mrl/1.0 "
                "http://standards.iso.org/iso/19115/-3/mrl/1.0/mrl.xsd "
                "http://standards.iso.org/iso/19115/-3/mrs/1.0 "
                "http://standards.iso.org/iso/19115/-3/mrs/1.0/mrs.xsd "
                "http://standards.iso.org/iso/19115/-3/msr/1.0 "
                "http://standards.iso.org/iso/19115/-3/msr/1.0/msr.xsd "
                "http://standards.iso.org/iso/19157/-2/mdq/1.0 "
                "http://standards.iso.org/iso/19157/-2/mdq/1.0/mdq.xsd "
                "http://standards.iso.org/iso/19115/-3/mac/1.0 "
                "http://standards.iso.org/iso/19115/-3/mac/1.0/mac.xsd "
                "http://standards.iso.org/iso/19115/-3/gco/1.0 "
                "http://standards.iso.org/iso/19115/-3/gco/1.0/gco.xsd "
                "http://standards.iso.org/iso/19115/-3/gmw/1.0 "
                "http://standards.iso.org/iso/19115/-3/gmw/1.0/gmw.xsd "
                "http://www.opengis.net/gml/3.2 "
                "http://schemas.opengis.net/gml/3.2.1/gml.xsd "
                "http://www.w3.org/1999/xlink http://www.w3.org/1999/xlink.xsd"
        },
        nsmap={
            "mdb": "http://standards.iso.org/iso/19115/-3/mdb/1.0",
            "xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "cat": "http://standards.iso.org/iso/19115/-3/cat/1.0",
            "gfc": "http://standards.iso.org/iso/19110/gfc/1.1",
            "cit": "http://standards.iso.org/iso/19115/-3/cit/1.0",
            "gcx": "http://standards.iso.org/iso/19115/-3/gcx/1.0",
            "gex": "http://standards.iso.org/iso/19115/-3/gex/1.0",
            "lan": "http://standards.iso.org/iso/19115/-3/lan/1.0",
            "srv": "http://standards.iso.org/iso/19115/-3/srv/2.0",
            "mas": "http://standards.iso.org/iso/19115/-3/mas/1.0",
            "mcc": "http://standards.iso.org/iso/19115/-3/mcc/1.0",
            "mco": "http://standards.iso.org/iso/19115/-3/mco/1.0",
            "mda": "http://standards.iso.org/iso/19115/-3/mda/1.0",
            "mds": "http://standards.iso.org/iso/19115/-3/mds/1.0",
            "mdt": "http://standards.iso.org/iso/19115/-3/mdt/1.0",
            "mex": "http://standards.iso.org/iso/19115/-3/mex/1.0",
            "mmi": "http://standards.iso.org/iso/19115/-3/mmi/1.0",
            "mpc": "http://standards.iso.org/iso/19115/-3/mpc/1.0",
            "mrc": "http://standards.iso.org/iso/19115/-3/mrc/1.0",
            "mrd": "http://standards.iso.org/iso/19115/-3/mrd/1.0",
            "mri": "http://standards.iso.org/iso/19115/-3/mri/1.0",
            "mrl": "http://standards.iso.org/iso/19115/-3/mrl/1.0",
            "mrs": "http://standards.iso.org/iso/19115/-3/mrs/1.0",
            "msr": "http://standards.iso.org/iso/19115/-3/msr/1.0",
            "mdq": "http://standards.iso.org/iso/19157/-2/mdq/1.0",
            "mac": "http://standards.iso.org/iso/19115/-3/mac/1.0",
            "gco": "http://standards.iso.org/iso/19115/-3/gco/1.0",
            "gml": "http://www.opengis.net/gml/3.2",
            "xlink": "http://www.w3.org/1999/xlink",
        }
    )

    mdb_md_metadata.append(make_xml_identifier("GeoNetwork UUID", "4fce6238-8d55-499c-bff5-98518552f4b4", "urn:uuid"))
    return etree.tostring(mdb_md_metadata, xml_declaration=True, encoding="UTF-8", pretty_print=True).decode()


def make_rdf(output_format: str = "ttl"):
    """Makes RDF from XML input"""
    if output_format not in RDF_FILE_TYPES:
        raise ValueError(f"output_format, if given, must be one of {', '.join(RDF_FILE_TYPES)}")

    g = Graph()
    g.add((URIRef("a:"), URIRef("b:"), URIRef("c:")))
    return g.serialize(format="longturtle" if output_format == "ttl" else output_format)


def main(input_file: Path, output_file: Path = None, output_format: str = "ttl", logging: bool = True):
    """The main function of this script.

    Can be called by other Python code or as a command line Python script"""
    global LOGGING
    if logging:
        if output_file:
            LOGGING = "stdout"
        else:
            LOGGING = "file"
    else:
        LOGGING = "none"

    log(f"Started processing {input_file}")

    # determine input file type
    if input_file.suffix == ".xml":
        log("Converting from XML")
        if output_format not in RDF_FILE_TYPES:
            raise ValueError(f"If converting from XML to RDF and supplying an RDF output format, it must be one of "
                             f"{', '.join(RDF_FILE_TYPES)}")

        rdf = make_rdf(output_format)
        if output_file is not None:
            open(output_file, "w").write(rdf)
        else:
            print(rdf)
    elif input_file.suffix.lstrip(".") in RDF_FILE_TYPES:
        log(f"Converting from RDF ({input_file.suffix.lstrip('.')})")

        xml = make_xml()
        if output_file is not None:
            open(output_file, "w").write(xml)
        else:
            print(xml)
    else:
        raise ValueError(f"Input file type is unknown. Must be either xml or one of {', '.join(RDF_FILE_TYPES)}")


if __name__ == "__main__":
    """Reads command line input and feeds it into the main() function    
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="{version}".format(version=__version__)
    )

    parser.add_argument(
        "input",
        help="Input file path",
        type=Path
    )

    parser.add_argument(
        "-o",
        "--outputfile",
        help="An output file path. If given, output will be written to this file. If not, output will be returned",
        type=Path,
        default=None,
    )

    parser.add_argument(
        "-f",
        "--outputformat",
        help=f"If converting XML to RDF, an RDF file format may be specified. "
             f"Must be one of {', '.join(RDF_FILE_TYPES)}. Default is ttl.",
        type=str,
        default="ttl",
    )

    parser.add_argument(
        "-l",
        "--log",
        help="If set, will print logging. If output_file is given, logging will be to std out, "
             "else to file processing.log",
        action=argparse.BooleanOptionalAction
    )

    args = parser.parse_args()

    main(args.input, args.outputfile, args.outputformat, args.log)
