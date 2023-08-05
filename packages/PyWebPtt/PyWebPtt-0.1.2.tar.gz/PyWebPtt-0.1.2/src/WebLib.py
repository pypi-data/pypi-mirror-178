import bs4
import urllib.request as req


class HttpClient:
    def obtainHeaders(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"
        }
        return headers

    def sendRequest(self, url, encoded="utf-8"):
        headers = self.obtainHeaders()
        URL = req.Request(url, headers=headers)
        with req.urlopen(URL) as res:
            pageData = res.read().decode(encoded)
        return pageData

#


class HtmlClient:
    def __init__(self):
        self.httpClient = HttpClient()

    def getHtml(self, url):
        pageData = self.httpClient.sendRequest(url)
        parsedData = bs4.BeautifulSoup(pageData, "lxml")
        return parsedData
