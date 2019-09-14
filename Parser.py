from bs4 import BeautifulSoup

class Parser:
   def __init__(self, htmlSource):
      self._soup = BeautifulSoup(htmlSource, "html.parser")

   def parseHtmlSource(self):
      metaTagsList = self._soup.find_all("meta")
      if (metaTagsList == None):
         return (False, 0)
      for metaTag in self._soup.find_all("meta"):
         if (metaTag.get("property") == "og:price:amount"):
            return (True, metaTag.get("content"))
      return (False, 0)


if __name__ == "__main__":
   fileObj = file("page_1.html", "r")
   source = fileObj.read()
   parser = Parser(source)
   parser.parseHtmlSource()
