import requests, json, datetime, sys, bs4, PyPDF2, os
from urllib.request import urlopen

with open(sys.argv[1]) as f:
    webpages = f.readlines()
webpages = [x.strip() for x in webpages]

for page in webpages:
    html = requests.get(page)
    soup = bs4.BeautifulSoup(html.text, "html.parser")
    outlinks = soup.find_all("a")
    links=[str(i.get('href')) for i in outlinks]
    outlinks = [str(i) for i in outlinks]
    docs=[] #docs is a list of lists in order: "name:", *name*, "text:", *text*

    for file in links:
        directory=page.rsplit("/",1)[0]
        link=directory+'/'+file

        if file.endswith(('txt')): #can be expanded to other file types with a comma
            text=bs4.BeautifulSoup(requests.get(link).text, "html.parser")
            text=["name:",link,"text:",text]
            docs.append(text)

        elif file.endswith(('pdf')): # special case if PDF
            pdf=file.rsplit("/",1)[-1]

            try:
                response = urlopen(link) # must first check if pdf is found

            except urllib.error.HTTPError as e:
                text=["name:",link,"text:","404"] #if 404 error, put 404 as text
                docs.append(text)

            else:
                file = open(pdf, 'wb') #otherwise must save the pdf to run pypdf2
                file.write(response.read())
                file.close()

                pdfFileObj = open(pdf, 'rb')
                pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
                pages=pdfReader.numPages

                j=0
                txt=""

                while j<pages:
                    pageObj = pdfReader.getPage(j)
                    txt+=pageObj.extractText()
                    j=j+1

                name=["name:",link,"text:", txt]
                os.remove(pdf) #remove the saved file when done
                docs.append(name)

        else: #if not supported file type, continue
            continue

    docs=[[str(i) for i in lis] for lis in docs]
    timestamp = datetime.datetime.now().isoformat()
    output = json.dumps({'url' : page, \
        'timestamp': timestamp, \
        'outlinks' : outlinks, \
        'html' : html.text, \
        'docs' : docs})
    print(output)
    print("\n")
