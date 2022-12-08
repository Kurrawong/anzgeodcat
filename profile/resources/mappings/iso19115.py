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
from lxml import etree


def make_identifier(title, code, code_space):
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


md_metadata = etree.Element(
    "{http://standards.iso.org/iso/19115/-3/mdb/1.0}MD_Metadata",
    {etree.QName("http://www.w3.org/2001/XMLSchema-instance", "schemaLocation"): "http://standards.iso.org/iso/19115/-3/cat/1.0 http://standards.iso.org/iso/19115/-3/cat/1.0/cat.xsd http://standards.iso.org/iso/19115/-3/cit/1.0 http://standards.iso.org/iso/19115/-3/cit/1.0/cit.xsd http://standards.iso.org/iso/19115/-3/gcx/1.0 http://standards.iso.org/iso/19115/-3/gcx/1.0/gcx.xsd http://standards.iso.org/iso/19115/-3/gex/1.0 http://standards.iso.org/iso/19115/-3/gex/1.0/gex.xsd http://standards.iso.org/iso/19115/-3/lan/1.0 http://standards.iso.org/iso/19115/-3/lan/1.0/lan.xsd http://standards.iso.org/iso/19115/-3/srv/2.0 http://standards.iso.org/iso/19115/-3/srv/2.0/srv.xsd http://standards.iso.org/iso/19115/-3/mas/1.0 http://standards.iso.org/iso/19115/-3/mas/1.0/mas.xsd http://standards.iso.org/iso/19115/-3/mcc/1.0 http://standards.iso.org/iso/19115/-3/mcc/1.0/mcc.xsd http://standards.iso.org/iso/19115/-3/mco/1.0 http://standards.iso.org/iso/19115/-3/mco/1.0/mco.xsd http://standards.iso.org/iso/19115/-3/mda/1.0 http://standards.iso.org/iso/19115/-3/mda/1.0/mda.xsd http://standards.iso.org/iso/19115/-3/mdb/1.0 http://standards.iso.org/iso/19115/-3/mdb/1.0/mdb.xsd http://standards.iso.org/iso/19115/-3/mds/1.0 http://standards.iso.org/iso/19115/-3/mds/1.0/mds.xsd http://standards.iso.org/iso/19115/-3/mdt/1.0 http://standards.iso.org/iso/19115/-3/mdt/1.0/mdt.xsd http://standards.iso.org/iso/19115/-3/mex/1.0 http://standards.iso.org/iso/19115/-3/mex/1.0/mex.xsd http://standards.iso.org/iso/19115/-3/mmi/1.0 http://standards.iso.org/iso/19115/-3/mmi/1.0/mmi.xsd http://standards.iso.org/iso/19115/-3/mpc/1.0 http://standards.iso.org/iso/19115/-3/mpc/1.0/mpc.xsd http://standards.iso.org/iso/19115/-3/mrc/1.0 http://standards.iso.org/iso/19115/-3/mrc/1.0/mrc.xsd http://standards.iso.org/iso/19115/-3/mrd/1.0 http://standards.iso.org/iso/19115/-3/mrd/1.0/mrd.xsd http://standards.iso.org/iso/19115/-3/mri/1.0 http://standards.iso.org/iso/19115/-3/mri/1.0/mri.xsd http://standards.iso.org/iso/19115/-3/mrl/1.0 http://standards.iso.org/iso/19115/-3/mrl/1.0/mrl.xsd http://standards.iso.org/iso/19115/-3/mrs/1.0 http://standards.iso.org/iso/19115/-3/mrs/1.0/mrs.xsd http://standards.iso.org/iso/19115/-3/msr/1.0 http://standards.iso.org/iso/19115/-3/msr/1.0/msr.xsd http://standards.iso.org/iso/19157/-2/mdq/1.0 http://standards.iso.org/iso/19157/-2/mdq/1.0/mdq.xsd http://standards.iso.org/iso/19115/-3/mac/1.0 http://standards.iso.org/iso/19115/-3/mac/1.0/mac.xsd http://standards.iso.org/iso/19115/-3/gco/1.0 http://standards.iso.org/iso/19115/-3/gco/1.0/gco.xsd http://standards.iso.org/iso/19115/-3/gmw/1.0 http://standards.iso.org/iso/19115/-3/gmw/1.0/gmw.xsd http://www.opengis.net/gml/3.2 http://schemas.opengis.net/gml/3.2.1/gml.xsd http://www.w3.org/1999/xlink http://www.w3.org/1999/xlink.xsd"},
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


# md_metadata.append(metadata_identifier)
# child2 = etree.SubElement(md_metadata, "child2")
# child2.text = "Child Two"
# child2.attrib["age"] = "12"

md_metadata.append(make_identifier("GeoNetwork UUID", "4fce6238-8d55-499c-bff5-98518552f4b4", "urn:uuid"))
print(etree.tostring(md_metadata, xml_declaration=True, encoding="UTF-8", pretty_print=True).decode())
