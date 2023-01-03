import os
import xml.etree.ElementTree as ET
import urllib.request
import json 
import time
import pickle 

# NOTE: Must use Python 3.9 for ET.indent

pmid_file = "pmid-augustinlu-set.txt"

with open(pmid_file) as f:
    pmid_ids = f.readlines()

pub_list = []

for i in range(len(pmid_ids)):
#for i in range(10):
    pmid_id = pmid_ids[i].strip()

    #pmid_id = "32460492"
    url = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={pmid_id}&rettype=xml'
    print(f'I: {i} URL: {url}')

    req = urllib.request.Request(
        url, 
        data=None, 
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        }
    )

    f = urllib.request.urlopen(req, timeout=60)
    xml = f.read()
    tree = ET.ElementTree(ET.fromstring(xml))

    journal = tree.find('.//ISOAbbreviation').text
    pub_year = tree.find('.//PubDate/Year').text
    pub_year = int(pub_year)
    title = tree.find('.//ArticleTitle').text

    abstract = ""
    try: 
        abstract = tree.find('.//AbstractText').text
    except:
        print(f'ERROR: {pmid_id}')
    
    pmid_url = f'http://www.ncbi.nlm.nih.gov/pubmed/{pmid_id}'

    tmp = {'title': title, 'year': pub_year, 'abstract': abstract, 'journal': journal, 'href': pmid_url, 'pmid': pmid_id}
    pub_list.append(tmp)

    time.sleep(1)

tmp_pub_list = sorted(pub_list, key = lambda i: i['year'])
tmp_pub_list.reverse()

pkl_file = open('publication_section.pkl', 'wb') 
pickle.dump(tmp_pub_list, pkl_file)
pkl_file.close()

section = ET.Element("section")
h1 = ET.SubElement(section, "h1").text = "Publications"

# <details>
#   <summary>TITLE (JOURNAL YEAR)</summary>
#   <p><strong>Link:</strong> <a href="https://pubmed.ncbi.nlm.nih.gov/33196823/">Pubmed</a></p>
#   <p><b>Abstract:</b> CellMiner Cross-Database (CellMinerCDB, discover.nci.nih.gov/cellminercdb) allows integration and analysis of molecular and pharmacological data within and across cancer cell line datasets from the National Cancer Institute (NCI), Broad Institute, Sanger/MGH and MD Anderson Cancer Center (MDACC). We present CellMinerCDB 1.2 with updates to datasets from NCI-60, Broad Cancer Cell Line Encyclopedia and Sanger/MGH, and the addition of new datasets, including NCI-ALMANAC drug combination, MDACC Cell Line Project proteomic, NCI-SCLC DNA copy number and methylation data, and Broad methylation, genetic dependency and metabolomic datasets. CellMinerCDB (v1.2) includes several improvements over the previously published version: (i) new and updated datasets; (ii) support for pattern comparisons and multivariate analyses across data sources; (iii) updated annotations with drug mechanism of action information and biologically relevant multigene signatures; (iv) analysis speedups via caching; (v) a new dataset download feature; (vi) improved visualization of subsets of multiple tissue types; (vii) breakdown of univariate associations by tissue type; and (viii) enhanced help information. The curation and common annotations (e.g. tissues of origin and identifiers) provided here across pharmacogenomic datasets increase the utility of the individual datasets to address multiple researcher question types, including data reproducibility, biomarker discovery and multivariate analysis of drug activity.</p>
# </details>

for i in range(len(tmp_pub_list)):
    item = tmp_pub_list[i]

    title = item['title']
    year = item['year']
    abstract = item['abstract']
    journal = item['journal']
    href = item['href']
    pmid = item['pmid']

    details = ET.SubElement(section, "details")
    ET.SubElement(details, "summary").text = f"{title} ({journal} {year})"

    p1 = ET.SubElement(details, "p")
    a1 = ET.SubElement(p1, "a", href=href).text = f"PMID: {pmid}"

    ET.SubElement(details, "p").text = abstract

tree = ET.ElementTree(section)
ET.indent(tree, space="  ", level=0)
tree.write("publication_section.xml")

# Example
## Output
# {
#     "name" : "PathVisio-MIM: PathVisio plugin for creating and editing Molecular Interaction Maps (MIMs).",
#     "date" : "2011",
#     "description" : "MOTIVATION: A plugin for the Java-based PathVisio pathway editor has been developed to help users draw diagrams of bioregulatory networks according to the Molecular Interaction Map (MIM) notation. Together with the core PathVisio application, this plugin presents a simple to use and cross-platform application for the construction of complex MIM diagrams with the ability to annotate diagram elements with comments, literature references and links to external databases. This tool extends the capabilities of the PathVisio pathway editor by providing both MIM-specific glyphs and support for a MIM-specific markup language file format for exchange with other MIM-compatible tools and diagram validation.\nAVAILABILITY: The PathVisio-MIM plugin is freely available and works with versions of PathVisio 2.0.11 and later on Windows, Mac OS X and Linux. Information about MIM notation and the MIMML format is available at http://discover.nci.nih.gov/mim. The plugin, along with diagram examples, instructions and Java source code, may be downloaded at http://discover.nci.nih.gov/mim/mim_pathvisio.html.\n",
#     "publisher" : "Bioinformatics (Oxford, England)",
#     "url" : "http://www.ncbi.nlm.nih.gov/pubmed/21636591",
#     "_id" : 1
# },

