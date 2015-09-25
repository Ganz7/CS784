import urllib2
import os

from bs4 import BeautifulSoup

def get_html_page(link):
	page = urllib2.urlopen(link)
	return page.read()

def download_and_save_movie_page(title, link, folder):
	page = get_html_page(link)
	#if not os.path.exists('/data/imdb'):
	#	os.makedirs('/data/imdb')
	with open(os.path.join('data/imdb', title), 'w+') as fid:
		fid.write(page)

def get_movie_titles(link):
	page_content = get_html_page(link)
	soup = BeautifulSoup(page_content, 'html.parser')

	#tables = soup.findAll("table", class_="wikitable sortable")
	#table = tables[0]
	#Get's the first table in the page with the matching classes
	table = soup.find("table", class_="wikitable sortable") 
	rows = table.findAll("tr")
	titles = []

	for row in rows:
		title_row = row.find("td")	
		if(title_row):
			title_tag = title_row.find("i").find("a")
			if(title_tag):
				titles.append(title_tag.text)

	return titles

def download_imdb_pages(titles):
	for title in titles:
		query_title = title.replace(" ", "+")
		query = "http://www.imdb.com/find?ref_=nv_sr_fn&q=" + query_title + "&s=tt"

		results_page = get_html_page(query)
		soup = BeautifulSoup(results_page, 'html.parser')
		first_results_row = soup.find("tr", class_="findResult odd") #Gets first result

		if(first_results_row):
			a_tag = first_results_row.find("a")
			link_to_movie = a_tag['href']
		
		link_to_movie = "http://imdb.com" + link_to_movie
		print link_to_movie
		download_and_save_movie_page(title, link_to_movie, "imdb")


def main():
	link = "https://en.wikipedia.org/wiki/List_of_American_films_of_2012"
	titles = get_movie_titles(link)
	x = ['Eternal Sunshine of the Spotless mind', "The Avengers"]
	download_imdb_pages(x)

if __name__ == '__main__':
	main()