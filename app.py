import cherrypy
import os
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('html'))

import get_yelp


class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        data_to_show = ['Hello', 'world']
        tmpl = env.get_template('index.html')
        return tmpl.render(data=data_to_show)

    @cherrypy.expose
    def scrape(self, city, search_term, ranking, number_of_pages):
        url_safe_search_term = search_term.replace(' ', '+')
        scraped_data = get_yelp.get_yelp(city, search_term, ranking,
                                         number_of_pages)
        cherrypy.response.headers['Content-Type'] = 'text/plain'
        cherrypy.response.headers[
            'Content-Disposition'] = "attachment; filename='scraped_data.txt'"
        cherrypy.response.headers['Content-Length'] = len(scraped_data)
        return scraped_data


config = {
    'global': {
        'server.socket_host': '0.0.0.0',
        'server.socket_port': int(os.environ.get('PORT', 5000)),
    },
    '/assets': {
        'tools.staticdir.root': os.path.dirname(os.path.abspath(__file__)),
        'tools.staticdir.on': True,
        'tools.staticdir.dir': 'assets',
    }
}

cherrypy.quickstart(HelloWorld(), '/', config=config)
