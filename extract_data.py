import os

from bs4 import BeautifulSoup

def extract_from_imdb_file(filename):
	print "Extracting ", filename
	file = open('data/imdb/' + filename, 'r')
	soup = BeautifulSoup(file, 'html.parser')
	
	print soup.title
	



	file.close()	

def extract_imdb_data():
	print "Extracting IMDB Movies data..."
	for filename in os.listdir('data/imdb/'):
		extract_from_imdb_file(filename)

def extract_rottentomatoes_data():
	print "Extracting Rotten Tomatoes Movies data..."

def main():
	extract_imdb_data()
	extract_rottentomatoes_data()

if __name__ == '__main__':
	main()