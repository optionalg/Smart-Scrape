import urllib.request

#Variables

pages = []

#Definitions

class Page(object):

	def __init__(self, url, source):
		self.url = url
		self.source = source
		

def get(page):
	
	#Perform some input validation
	if ("http://" not in page):
		page = "http://" + page

	#Get the page
	response = urllib.request.urlopen(page)
	html = response.read()
	html = html.decode("utf8")
	response.close

	#Format the code for printing with tabs and new lines
	formattedHtml = ""
	tabNo = 0
	for c in html:
		if (c == ">" or c == ";"):
			formattedHtml += c
			formattedHtml += "\n" + (tabNo * "\t")
		elif (c == "{"):
			tabNo += 1
			formattedHtml += c
			formattedHtml += "\n" + (tabNo * "\t")
		elif (c == "}"):
			tabNo -= 1
			formattedHtml += "\n" + (tabNo * "\t")
			formattedHtml += c
		else:
			formattedHtml += c
			
	return formattedHtml
	
def search(htmlIn, search):
	
	searched = ""
	
	#adjust for self closing tags
	if (search != "img"):
		start = htmlIn.find("<" + search)
		end = htmlIn.find("</" + search + ">") + len(search)
	else:
		start = htmlIn.find("<" + search)
		end = htmlIn[start:].find(">")
		
	#Keep going until no more tags can be found
	while (start != -1 and end != -1):
		link = htmlIn[start:end]
		searched += link
		htmlIn = htmlIn[end+len(search):]
		
		
		#adjust for self closing html tags
		if (search != "img"):
			start = htmlIn.find("<" + search)
			end = htmlIn.find("</" + search + ">") + len(search)
		else:
			start = htmlIn.find("<" + search)
			end = htmlIn[start:].find(">")
	
	return searched
	
def links(htmlIn):
	
	linksString = ""

	start = htmlIn.find("href=\"")
	htmlIn = htmlIn[start + 6:]
	end = htmlIn.find("\"")
		
	#Keep going until no more links can be found
	while (start != -1 and end != -1):
	
		link = htmlIn[0:end]
		
		if(link not in linksString):
			linksString += link + "\n"
		
		htmlIn = htmlIn[end + 1:]
		start = htmlIn.find("href=\"")
		htmlIn = htmlIn[start + 6:]
		end = htmlIn.find("\"")
	
	return linksString
	
	
	
def count(htmlIn, search):

	counter = 0
	
	#adjust for self closing tags
	if (search != "img"):
		start = htmlIn.find("<" + search)
		end = htmlIn.find("</" + search + ">") + len(search)
	else:
		start = htmlIn.find("<" + search)
		end = htmlIn[start:].find("/>")
		
	#Keep going until no more tags can be found
	while (start != -1 and end != -1):
		link = htmlIn[start:end]
		counter += 1
		htmlIn = htmlIn[end+len(search):]
		
		
		#adjust for self closing html tags
		if (search != "img"):
			start = htmlIn.find("<" + search)
			end = htmlIn.find("</" + search + ">") + len(search)
		else:
			start = htmlIn.find("<" + search)
			end = htmlIn[start:].find("/>")
	
	return counter
	
def startMenu():		
	print("--- Smart Scrape ---")
	print("Please enter a website or type exit")
	
def siteMenu(site):
	print("The website at " + site.url + ":\n\nSource Length: " + str(len(site.source)))
	print("Script Tags: " + str(count(site.source, "script")))
	print("Javascript Length:" + str(len(search(site.source, "script"))) + "\n")
	print("Link Tags: " + str(count(site.source, "a")) + "\n")
	print("Links: " + links(site.source) + "\n")
	print("Images: " + str(count(site.source, "img")))
	
#Program Loop

startMenu()
address = input("Enter Address: ")

if (address != "exit"):
	pages.append(Page(address, get(address)))
	siteMenu(pages[len(pages) - 1])