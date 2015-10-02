import urllib2
import os
import sys
import re

from bs4 import BeautifulSoup

def get_html_page(link):
	page = urllib2.urlopen(link)
	return page.read()

def remove_non_alphanumeric_chars(str):
	return re.sub(r'\W+', ' ', str)

def download_and_save_movie_page(title, link, folder):
	page = get_html_page(link)
	#if not os.path.exists('/data/imdb'):
	#	os.makedirs('/data/imdb')
	with open(os.path.join('data/' + folder, title), 'w+') as fid:
		fid.write(page)

#Returns all the titles from the give wikipedia page
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
				condensed_title = remove_non_alphanumeric_chars(title_tag.text)
				titles.append(condensed_title)

	return titles

def download_rottentomatoes_pages(titles):
	for title in titles:
		print "Getting rottentomatoes movie ", title
		query_title = title.replace(" ", "+")
		query = "http://www.rottentomatoes.com/search/?search=" + query_title
		link_to_movie = ""

		results_page = get_html_page(query)
		soup = BeautifulSoup(results_page, 'html.parser')
		#print soup.prettify()

		#We are in the search page
		#Get the first result from the search page and save that.
		if "Search Results" in soup.title.text:
			span = soup.find("span", class_="movieposter")
			#li = ul.find("li")
			if(span):
				a_tag = span.find("a")
				link_to_movie = a_tag['href']
				link = "http://rottentomatoes.com" + link_to_movie
				download_and_save_movie_page(title , link, "rottentomatoes")

		#We are directly in the movie page
		else:
			with open(os.path.join('data/rottentomatoes', title), 'w+') as fid:
				fid.write(results_page)
		

def download_imdb_pages(titles):
	for title in titles:
		print "Getting imdb movie ", title
		query_title = title.replace(" ", "+")
		query = "http://www.imdb.com/find?ref_=nv_sr_fn&q=" + query_title + "&s=tt"
		link_to_movie = ""

		#Get the first result from the search page and save that.
		results_page = get_html_page(query)
		soup = BeautifulSoup(results_page, 'html.parser')
		first_results_row = soup.find("tr", class_="findResult odd") 

		if(first_results_row):
			a_tag = first_results_row.find("a")
			link_to_movie = a_tag['href']
		
		link = "http://imdb.com" + link_to_movie
		#print link
		download_and_save_movie_page(title , link, "imdb")


def main(from_year, to_year):
	link = "https://en.wikipedia.org/wiki/List_of_American_films_of_"
	for x in range(int(from_year), int(to_year)+1):
		print link+str(x)
		titles = get_movie_titles(link+str(x))
		#titles = ['Eternal Sunshine of the Spotless mind', 'The Avengers']
		download_imdb_pages(titles)
		download_rottentomatoes_pages(titles)

if __name__ == '__main__':
	if len(sys.argv) < 3:
		print "Usage: Python download_pages.py <start_year> <end_year>"
		sys.exit(0)
	main(sys.argv[1], sys.argv[2])