from selenium import webdriver
import os, re, time, sqlite3

connect = sqlite3.connect('movie_list.db')
c = connect.cursor()
c.execute('CREATE TABLE IF NOT EXISTS movies(\'month\',\'titles\')')

driver = webdriver.Chrome(r'C:\Users\leosc\Downloads\chromedriver')

driver.get('https://www.imdb.com/movies-in-theaters/?ref_=ft_inth')



class Movie():
	def __init__(self):
		self.date_of_release = re.findall('(\w+\s+\d+)', driver.find_element_by_xpath('//*[contains(text(), \'Opening This Week\')]').get_attribute('innerHTML'))
		self.new_movies_webelement = driver.find_elements_by_xpath('//*[contains(text(), \'Opening This Week\')]/following-sibling::*/child::*//*[contains(@class, \'overview-top\')]/h4/child::*')
		self.new_movies_titles = [movie.get_attribute('title') for movie in self.new_movies_webelement]
		self.movies_in_list = open(r'C:\Users\leosc\AppData\Local\Programs\Python\Python37-32\Projects\WebCrawler\movies.txt', 'r').readlines()
	
	# @classmethod
	# def return_movie_in_list(self):
		# movie_list_file_read =  open(r'C:\Users\leosc\AppData\Local\Programs\Python\Python37-32\Projects\WebCrawler\movies.txt', 'r')
		# movies = movie_list_file_read.readlines()
		# return movies
	
	@classmethod
	def write_movies_to_list(self):
		if os.path.isfile(r'C:\Users\leosc\AppData\Local\Programs\Python\Python37-32\Projects\WebCrawler\movies.txt'):
			movie_list_file = open(r'C:\Users\leosc\AppData\Local\Programs\Python\Python37-32\Projects\WebCrawler\movies.txt', 'a+')
		else:
			movie_list_file =  open(r'C:\Users\leosc\AppData\Local\Programs\Python\Python37-32\Projects\WebCrawler\movies.txt', 'w+')
			
		m = Movie()
		
		titles = '\n'.join(m.new_movies_titles)#[items for items in m.new_movies_titles if items not in m.movies_in_list])
		date_of_release = m.date_of_release[0]
		
		for title in m.new_movies_titles:
			c.executemany('INSERT INTO movies VALUES ('\''+date_of_release+'\'','\''+titles'\'')
		
		movie_list_file.write('\n' + '\''+date_of_release+'\'' + ': \n' + '\''+titles'\'')
								
		movie_list_file.close()
while True:
	Movie.write_movies_to_list()
	time.sleep(86400)
