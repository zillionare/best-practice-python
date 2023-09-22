import fire
import markdown
from bs4 import BeautifulSoup
from docxtpl import DocxTemplate, InlineImage, RichText

# https://stackoverflow.com/questions/70363269/how-can-i-convert-a-markdown-string-to-a-docx-in-python


def mark2html(value):
    if value == None:
        return "-"
    html = markdown.markdown(value)
    soup = BeautifulSoup(html, features="html.parser")
    paragraphs = []
    global doc
    for tag in soup.findAll(True):
        if tag.name in ("p", "h1", "h2", "h3", "h4", "h5", "h6"):
            paragraphs.extend(parseHtmlToDoc(tag))
    return paragraphs


def parseHtmlToDoc(org_tag):
    global doc
    contents = org_tag.contents
    pars = []
    for con in contents:
        if str(type(con)) == "<class 'bs4.element.Tag'>":
            tag = con
            if tag.name in ("strong", "h1", "h2", "h3", "h4", "h5", "h6"):
                source = RichText("")
                if (
                    len(pars) > 0
                    and str(type(pars[len(pars) - 1]))
                    == "<class 'docxtpl.richtext.RichText'>"
                ):
                    source = pars[len(pars) - 1]
                    source.add(con.contents[0], bold=True)
                else:
                    source.add(con.contents[0], bold=True)
                    pars.append(source)
            elif tag.name == "img":
                source = tag["src"]
                imagen = InlineImage(doc, source)
                pars.append(imagen)
            elif tag.name == "em":
                source = RichText("")
                source.add(con.contents[0], italic=True)
                pars.append(source)
        else:
            source = RichText("")
            if (
                len(pars) > 0
                and str(type(pars[len(pars) - 1]))
                == "<class 'docxtpl.richtext.RichText'>"
            ):
                source = pars[len(pars) - 1]
                pars.append(con)
            else:
                if org_tag.name == "h2":
                    source.add(con, bold=True, size=40)
                else:
                    source.add(con)
                pars.append(source)  # her zaman append?
    return pars


def convert(file: str):
    with open(file, "r") as f:
        content = f.readlines()
