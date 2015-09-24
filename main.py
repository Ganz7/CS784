import urllib2
from bs4 import BeautifulSoup

def get_html_page(link):
	page = urllib2.urlopen(link)
	return page.read()

def get_movie_pages(link):
	page_content = get_html_page(link)
	soup = BeautifulSoup(page_content, 'html.parser')

	#tables = soup.findAll("table", class_="wikitable sortable")
	#table = tables[0]
	table = soup.find("table", class_="wikitable sortable")
	rows = table.findAll("tr")
	titles = []

	for row in rows:
		title_row = row.find("td")	
		if(title_row):
			title_tag = title_row.find("i").find("a")
			if(title_tag):
				titles.append(title_tag.text)

	for title in titles:
		print title


def main():
	link = "https://en.wikipedia.org/wiki/List_of_American_films_of_2012"
	get_movie_pages(link)

if __name__ == '__main__':
	main()