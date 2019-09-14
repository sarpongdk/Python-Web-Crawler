import os
import subprocess
import random
import time
import pip

from ProxiesService import ProxiesService
from Parser import Parser
from bs4 import BeautifulSoup

class Crawler:
   def __init__(self, proxyService, url):
      self._proxyService = proxyService
      self._url = url
      self._sleepDuration = 1
      self._cost = []

   def generateRoomNumber(self, start = 111111, end = 911619):
      return random.randint(start, end)

   def formatRequestUrl(self):
      room = self.generateRoomNumber()
      url = self._url + str(room) + "?noDates=true"
      return url

   def chooseRandomProxy(self):
      index = random.randint(0, self._proxyService.getNumberOfAvailableProxies())
      return self._proxyService.getProxy(index)

   def crawl(self, maxCount):
      costList = []
      count = 0
      pageNumber = 0
      while (count < maxCount):
         print "Downloading page %d..." % (pageNumber)
         command = "curl -p %s -b cookiefile.txt -L -m 10 -H 'Connection: keep-alive\\' -H 'Accept-Language: en-us, en; q=0.5' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'X-Requested-With: XMLHttpRequest' --stderr errorFile.txt --user-agent 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1 Safari/605.1.15' %s" %( self.chooseRandomProxy(), self.formatRequestUrl() )
         commandList = command.split()
         htmlSource = subprocess.check_output(command, shell=True, stderr = subprocess.STDOUT)
         print "Parsing page %d..." % (pageNumber)
         isRoom, cost = self.parseUserFiles(htmlSource)
         if (isRoom):
            costList.append(float(cost))
            count += 1
            pageNumber += 1
            self.saveHtmlPage(pageNumber, htmlSource)
         else:
            print "Page %d was not a valid page" %( pageNumber )
            print "Re-downloading another page as page %d..." %( pageNumber )
         time.sleep(self._sleepDuration)
      return costList

   def parseUserFiles(self, source):
      soup = BeautifulSoup(source, "html.parser")
      metaTagsList = soup.find_all("meta")
      if (metaTagsList == None):
         return (False, 0)
      for metaTag in soup.find_all("meta"):
         if (metaTag.get("property") == "og:price:amount"):
            return (True, metaTag.get("content"))
      return (False, 0)

   def calculateMean(self, costs):
      return float(sum(costs))/len(costs)

   def calculateVariance(self, costs, mean):
      variance = sum((cost - mean)**2 for cost in costs)/len(costs)
      return variance

   def saveHtmlPage(self, pageNumber, source):
      print "Saving html page...\n"
      filename = "page_%d.html" %( pageNumber )
      fileObj = open(filename, "w")
      fileObj.write(source)
      fileObj.close()

   def writeToFile(self, filename, costs, mean, variance):
      print "Writing output to file: %s" %( filename )
      fileObj = open(filename, "w")
      fileObj.write("Cost: [%s]\nVariance: %.2f\nMean: %.2f\n" %(", ".join(map(str, costs)), variance, mean))
      fileObj.close()
      return True

if __name__ == "__main__":
   service = ProxiesService(["5.32.131.98:53792", "103.217.156.9:8080", "14.232.245.221:8080", "200.127.220.21:8080", "167.99.40.249:80", "134.119.205.248:8080", "177.67.8.223:48314"])
   url = "https://www.vrbo.com/"
   crawler = Crawler(service, url)
   costs = crawler.crawl(10)
   mean = crawler.calculateMean(costs)
   variance = crawler.calculateVariance(costs, mean)
   crawler.writeToFile("outputFile.txt", costs, mean, variance)
   print "Costs Distribution: [%s]" %( ", ".join(map(str, costs)) ) 
   print "Mean: %.2f" %(mean)
   print "Variance: %.2f" %(variance)



