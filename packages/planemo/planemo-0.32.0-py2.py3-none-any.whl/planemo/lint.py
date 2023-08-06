import os

import requests

from six.moves.urllib.error import (
    HTTPError,
    URLError,
)
from six.moves.urllib.request import (
    urlopen,
)

from planemo.shed import find_urls_for_xml
from planemo.xml import validation


def lint_dois(tool_xml, lint_ctx):
    dois = find_dois_for_xml(tool_xml)
    for publication in dois:
        is_doi(publication, lint_ctx)


def find_dois_for_xml(tool_xml):
    dois = []
    for element in tool_xml.getroot().findall("citations"):
        for citation in list(element):
            if citation.tag == 'citation' and citation.attrib.get('type', '') == 'doi':
                dois.append(citation.text)
    return dois


def is_doi(publication_id, lint_ctx):
    """
    Check if dx.doi knows about the publication_id
    """
    base_url = "http://dx.doi.org"
    doiless_publication_id = publication_id.split("doi:", 1)[-1]
    url = "%s/%s" % (base_url, doiless_publication_id)
    r = requests.get(url)
    if r.status_code == 200:
        if publication_id != doiless_publication_id:
            lint_ctx.error("%s is valid, but Galaxy expects DOI without 'doi:' prefix" % publication_id)
        else:
            lint_ctx.info("%s is a valid DOI" % publication_id)
    elif r.status_code == 404:
        lint_ctx.error("%s is not a valid DOI" % publication_id)
    else:
        lint_ctx.warn("dx.doi returned unexpected status code %d" % r.status_code)


def lint_xsd(lint_ctx, schema_path, path):
    name = os.path.basename(path)
    validator = validation.get_validator(require=True)
    validation_result = validator.validate(schema_path, path)
    if not validation_result.passed:
        msg = "Invalid %s found. Errors [%s]"
        msg = msg % (name, validation_result.output)
        lint_ctx.error(msg)
    else:
        lint_ctx.info("%s found and appears to be valid XML" % name)


def lint_urls(root, lint_ctx):
    urls = find_urls_for_xml(root)

    def validate_url(url, lint_ctx):
        is_valid = True
        try:
            handle = urlopen(url)
            handle.read(100)
        except HTTPError as e:
            if e.code == 429:
                # too many requests
                pass
            else:
                is_valid = False
                lint_ctx.error("HTTP Error %s accessing %s" % (e.code, url))
        except URLError as e:
            is_valid = False
            lint_ctx.error("URL Error %s accessing %s" % (str(e), url))
        if is_valid:
            lint_ctx.info("URL OK %s" % url)

    for url in urls:
        validate_url(url, lint_ctx)
