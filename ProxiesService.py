class ProxiesService:
   def __init__(self, proxies = None):
      if (proxies is None):
         self._proxies = []
      else:
         self._proxies = proxies

   def addProxyUrl(self, proxy):
      self._proxies.append(proxy)

   def getProxies(self):
      return self._proxies

   def isEmpty(self):
      if (len(self._proxies) == 0):
         return True
      else:
         return False

   def setProxies(self, proxies):
      if (proxies is None or type(proxies) != list):
         return
      self._proxies = proxies

   def getNumberOfAvailableProxies(self):
      return len(self._proxies)

   def getProxy(self, index):
      if (index >= len(self._proxies) or index < 0):
         return self._proxies[len(self._proxies) - 1]
      else:
         return self._proxies[index]

if __name__ == "__main__":
   service = ProxiesService()
   print service.isEmpty()
   service.addProxyUrl("127.0.0.1:8080")
   for proxy in service.getProxies():
      print proxy

