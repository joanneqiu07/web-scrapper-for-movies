# to run 
# scrapy crawl tmdb_spider -o movies.csv

import scrapy

class TmdbSpider(scrapy.Spider):
    name = 'tmdb_spider'
    
    start_urls = ['https://www.themoviedb.org/movie/374720-dunkirk/']

    def parse(self, response):
        '''
        parse the page of a movie, find the link to the full cast & crew page,
        and navigate to that page
        '''
        
        # hardcode the link to the full cast & crew page
        link = response.url + '/cast/'

        # use scrapy.Request() to naviage to the page
        yield scrapy.Request(link, callback=self.parse_full_credits)


    def parse_full_credits(self, response):
        '''
        parse the full cast & crew page, find the links to all the actors' pages,
        and naviagate to each of the pages
        '''

        # use response.css to filter out the crew and save only the cast
        cast = response.css("ol.people.credits:not(ol.people.credits.crew)")
        links = cast.css("li div.info a::attr(href)").getall()
        
        # genearte the full urls
        for link in links:
            url = "https://themoviedb.org" + link
            yield scrapy.Request(url, callback=self.parse_actor_page)

        
    def parse_actor_page(self, response):
        '''
        parse the actor page, find the actor's name and 
        the names of all movies or tv shows on which the actor has worked
        '''

        # get the name of the actor and the names of all movies or tv shows
        actor_name = response.css("div.title h2 a::text").get()
        movie_or_TV_names = response.css("h3.zero + table.card.credits a.tooltip bdi::text").getall()

        # yield the names
        for movie_or_TV_name in movie_or_TV_names:
            yield {"actor" : actor_name, "movie_or_TV_name" : movie_or_TV_name}
