import requests
import json
import datetime
import sys
import bs4
import os
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
from pdfminer.converter import PDFPageAggregator
from urllib.request import urlopen
from urllib.parse import urlparse
from reppy.robots import Robots
import urllib.error

import Crawling_L_REST
api_url = 'https://crawling-team-l-braune131.c9users.io'
# =========================================================
# Get's webpage URLs from a file -- used for testing only


def get_webpages(filename):
    with open(filename) as f:
        webpages = f.readlines()
    webpages = [x.strip() for x in webpages]
    return webpages

# =========================================================
# Gets webpage data from a given URL

''' parse_webpages:
    parse_webpages is given a list of webpages and it will
    check if the crawler is allowed to crawl that page from
    the robots.txt file.  If it is allowed to crawl, it will
    obtain the sitemaps from that page, the html of the page,
    the links from the page, and all the documents from that
    page. '''
def parse_webpages(webpages):
    for page in webpages:
        # obtain the robots.txt url
        r = Robots.robots_url(page)
        robots = Robots.fetch(r)
        if(robots.allowed(page, '*')):
            # sitemaps is a list of all the sitemaps for a website
            sitemaps = robots.sitemaps
            sitemaps_list = list(sitemaps)
            html = requests.get(page) # html of the webpage
            soup = bs4.BeautifulSoup(html.text, "html.parser")
            outlinks = soup.find_all("a") # all the outlinks
            links = [str(i.get('href')) for i in outlinks]
            outlinks = [str(i) for i in outlinks]
            docs = [] # the documents on the page

            for file in links:
                directory = page.rsplit("/", 1)[0]
                link = directory + '/' + file

                # can be expanded to other file types with a comma
                if file.endswith(('txt', 'md')):
                    if file.startswith(('http://', 'www.')):
                        text = bs4.BeautifulSoup(
                            requests.get(file).text, "html.parser")
                        ext = file.rsplit(".", 1)[-1]
                        text = [file, ext, text]
                        # text = {'link': link, 'ext': ext, 'text': text}
                        docs.append(text)
                    else:
                        text = bs4.BeautifulSoup(
                            requests.get(link).text, "html.parser")
                        ext = link.rsplit(".", 1)[-1]
                        text = [link, ext, text]
                        # text = {'link': link, 'ext': ext, 'text': text}
                        docs.append(text)
                elif file.endswith(('pdf')):  # special case if PDF
                    x = file
                    try:
                        if file.startswith(('http://', 'www.')):
                            pdf = file.rsplit("/", 1)[-1]
                            response = urlopen(file)
                        else:
                            pdf = file.rsplit("/", 1)[-1]
                            # must first check if pdf is found
                            response = urlopen(link)

                    except urllib.error.HTTPError as e:
                        # if 404 error, put 404 as text
                        text = [link, "pdf", "404"]
                        # text = {'link': link, 'ext': 'pdf', 'text': "404"}
                        docs.append(text)

                    else:
                        # otherwise must save the pdf to run pypdf2
                        file = open(pdf, 'wb')
                        file.write(response.read())
                        file.close()
                        if x.startswith('http://'):
                            link = x
                        txt = ""
                        file = open(pdf, 'rb')
                        parser = PDFParser(file)
                        document = PDFDocument(parser)
                        rsrcmgr = PDFResourceManager()
                        laparams = LAParams()
                        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
                        interpreter = PDFPageInterpreter(rsrcmgr, device)
                        for p in PDFPage.create_pages(document):
                            # As the interpreter processes the page stored in PDFDocument object
                            interpreter.process_page(p)
                            # The device renders the layout from interpreter
                            layout = device.get_result()
                            # Out of the many LT objects within layout, we are interested in LTTextBox and LTTextLine
                            for lt_obj in layout:
                                if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                                    txt += lt_obj.get_text()

                        # close the pdf file
                        file.close()
                        name = [link, "pdf", txt]
                        # name = {'link': link, 'ext': 'pdf', 'text': txt}
                        os.remove(pdf)  # remove the saved file when done
                        docs.append(name)

            docs = [[str(i) for i in lis] for lis in docs]
            timestamp = datetime.datetime.now().isoformat()
            output = {'url': page,
                      'timestamp': timestamp,
                      'outlinks': outlinks,
                      'html': html.text,
                      'docs': docs,
                      'sitemaps': sitemaps_list}

            with Crawling_L_REST.app.app_context():
                Crawling_L_REST.add_webpage(output)

            return output

# =======================================================================================================
# Main


if __name__ == '__main__':
    webpages = get_webpages(sys.argv[1])
    print(webpages)
    print('\n\n')
    output = parse_webpages(webpages)
    print(output)
