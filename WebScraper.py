from bs4 import BeautifulSoup
from requests_html import HTMLSession
import sys

URL = "https://www.bbc.com/news/world-us-canada-65649229"

session = HTMLSession()
request = session.get(URL)
request.html.render(timeout=120)
soup = BeautifulSoup(request._content, "html.parser")


# turn navbar into hidden section
if soup.find("nav"):
    navBars = soup.find_all("nav")
    hiddenNav = BeautifulSoup(f"<details id='hiddenNav' style='background-color:lightgrey'> <summary style='background-color:white'><b>Navigation Bar</b></summary> {''.join(str(navBar) for navBar in navBars)} </details>", "lxml")
    soup.nav.replace_with(hiddenNav)

    for i in soup.find_all("nav"):
        if i.parent.name != "details":
            i.decompose()


# turn footer into hidden section
if soup.find("footer"):
    footers = soup.find_all("footer")
    hiddenFooter = BeautifulSoup(f"<details id='hiddenFooter' style='background-color:lightgrey'> <summary style='background-color:white'><b>Footer</b></summary> {''.join(str(footer) for footer in footers)} </details>", "lxml")
    soup.footer.replace_with(hiddenFooter)

    for i in soup.find_all("footer"):
        if i.parent.name != "details":
            i.decompose()


# remove images
for image in soup.find_all("img"):
    if alt:=image.attrs.get("alt"):
        imageParagraph = BeautifulSoup(f"<p style='background: rgba(255, 255, 255, 0.5);'><i>Image removed. Alt text: {alt}</i></p>", "lxml")
    else:
        imageParagraph = BeautifulSoup("<p style='background: rgba(255, 255, 255, 0.5);'><i>Image Removed</i></p>", "lxml")

    image.replace_with(imageParagraph)


# remove icons (svg)
for icon in soup.find_all("svg"):
    if alt:=icon.attrs.get("alt"):
        iconParagraph = BeautifulSoup(f"<p style='background: rgba(255, 255, 255, 0.5);'><i>Icon removed. Alt text: {alt}</i></p>", "lxml")
    else:
        iconParagraph = BeautifulSoup("<p style='background: rgba(255, 255, 255, 0.5);'>⍰</p>", "lxml")

    icon.replace_with(iconParagraph)


# remove videos
for video in soup.find_all("video"):
    video.replace_with(BeautifulSoup(f"<p style='background: rgba(255, 255, 255, 0.5);'><i>Video removed</i></p>", "lxml"))


# remove embed
for iframe in soup.find_all("iframe") + soup.find_all("embed"):
    if title:=iframe.attrs.get("title"):
        iframeParagraph = BeautifulSoup(f"<p style='background: rgba(255, 255, 255, 0.5);'><i>Embed removed. Title: {title}</i></p>", "lxml")
    else:
        iframeParagraph = BeautifulSoup("<p style='background: rgba(255, 255, 255, 0.5);'><i>Embed removed.</i></p>", "lxml")

    iframe.replace_with(iframeParagraph)


# remove references to files from links & removes scripts
for reference in soup.find_all("link") + soup.find_all("script"):
    reference.decompose()

print(soup.prettify())

# file = open("websiteOutput.html", "w", encoding="utf-8")
# file.write(soup.prettify())
# file.close()


# not working: 
# - the guardian, images r getting through, i believe this is bc they're loaded by javascript
# - al jazeera, returns a blank page unless the links are kept
