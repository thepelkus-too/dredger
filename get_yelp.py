from bs4 import BeautifulSoup
import requests
"""
get_yelp() prompts the user to choose a city and a search term. The program uses Yelp's search function
and pulls up the page for the top non-sponsored result and collects the text from however many pages of reviews the
user asks for.
"""

# this variable maps city names (as they will be displayed to the user) to Yelp's city codes as they appear in urls
# used later on for constructing the urls to visit
cities = {
    'chicago': 'Chicago,+IL',
    'new york': 'New+York,+NY',
    'london': 'London,+United+Kingdom'
}


def get_city_from_user():
    # get the city part to put in the search url
    city_list = list(cities.keys())
    for i in range(len(city_list)):
        print("%s %s" % (i + 1, city_list[i]))

    choice = input('Choose a city by number:\n')
    city = city_list[int(choice) - 1]
    city_string = cities[city]

    return city_string


def get_search_term_from_user():
    search_term = input('Enter search term:\n')
    search_term_string = search_term.replace(' ', '+')
    return search_term_string


def get_rating_category_from_user():
    ratings = {
        'high': '&sort_by=rating_desc',
        'low': '&sort_by=rating_asc',
        'average': ''
    }

    rating_list = list(ratings.keys())
    for i in range(len(rating_list)):
        print("%s %s" % (i + 1, rating_list[i]))

    choice = input('High or low rating:\n')
    city = rating_list[int(choice) - 1]
    rating_suffix = ratings[city]
    return rating_suffix


def get_number_of_pages_from_user():
    return input('How many pages of results?\n')


def get_destination_from_user():
    return input('Choose save name:\n')


def write_results_to_file(results, basename):
    outfilename = "texts/%s.txt" % basename
    outfile = open(outfilename, 'w', encoding='utf-8')
    outfile.write(results)


def command_line_search():
    city_string = get_city_from_user()
    search_term_string = get_search_term_from_user()
    rating_suffix = get_rating_category_from_user()
    num_pages = get_number_of_pages_from_user()
    destination = get_destination_from_user()

    scraped_text = get_yelp(city_string, search_term_string, rating_suffix,
                            num_pages)

    write_results_to_file(scraped_text, destination)


def get_yelp(city_string, search_term_string, rating_suffix, num_pages):
    search_url = 'https://www.yelp.com/search?find_desc=%s&find_loc=%s' % (
        search_term_string, city_string)

    page = requests.get(search_url).text
    soup = BeautifulSoup(page, "html.parser")
    foo = soup.findAll(class_='indexed-biz-name')
    # get the link to the top search result page

    for f in foo:
        if f.get_text()[0:2] == '1.':
            print("Link should be assigned")
            link = f.contents[1]['href']  # link from top search result
            break

    url_list = []
    for n in range(0, int(num_pages) * 20, 20):
        url = "https://www.yelp.com%s?start=%s%s" % (link, n, rating_suffix)
        url_list.append(url)

    scraped_text = ""
    for url in url_list:
        print(url)
        page = requests.get(url).text
        soup = BeautifulSoup(page, "html.parser")
        foo = soup.findAll(itemprop="description")
        for x in foo:
            scraped_text += x.get_text()
    return scraped_text


if __name__ == "__main__":
    command_line_search()
