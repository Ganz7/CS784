import urllib2
from bs4 import BeautifulSoup

def get_html_page(link):
	page = urllib2.urlopen(link)
	return page.read()

def get_movie_pages(link):
	page_content = get_html_page(link)
	soup = BeautifulSoup(page_content, 'html.parser')

	print soup.title

def main():
	link = "https://en.wikipedia.org/wiki/List_of_American_films_of_2012"
	get_movie_pages(link)

if __name__ == '__main__':
	main()