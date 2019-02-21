# Load libraries
import requests
from bs4 import BeautifulSoup
import copy
import json

# Creates a list to store the movies
db_test = []


# Function to get birth country of a person
def get_birth_country(link):
    url = 'https://www.imdb.com' + link
    response_bio = requests.get(url, headers={"Accept-Language": "en-US, en;q=0.5"})
    html_bio = BeautifulSoup(response_bio.text, 'html.parser')

    if html_bio.find('div', id="name-born-info") is not None:
        country = list(html_bio.find('div', id="name-born-info"))[-2].text
        country = country.split(',')[-1].strip()
        return country
    else:
        return 'NA'


# Funcion to get the gender of a person
def get_gender(name):
    name_string = '+'.join(name.split())
    url_gender_female = 'https://www.imdb.com/search/name?name=' + name_string + '&gender=female'
    response_gender = requests.get(url_gender_female, headers={"Accept-Language": "en-US, en;q=0.5"})
    html_gender = BeautifulSoup(response_gender.text, 'html.parser')

    if html_gender.find('div', class_='desc') is not None:
        result_gender = html_gender.find('div', class_='desc')
        result_gender = result_gender.text.strip().replace('.', "")
        if result_gender == 'No results':
            return 'Male'
        else:
            return 'Female'
    else:
        return 'NA'


def get_data(num_movies):
    starts = [str(i) for i in range(1, num_movies, 250)]

    # Get database
    for start in starts:

        # Creates the url to be searched
        url = 'https://www.imdb.com/search/title?title_type=feature&sort=boxoffice_gross_us,desc&count=250&start=' + \
              start + '&ref_=adv_nxt'
        # Make a get request
        response = requests.get(url, headers={"Accept-Language": "en-US, en;q=0.5"})

        # Parse the request contact into BeautifulSoup object
        html_soup = BeautifulSoup(response.text, 'html.parser')

        # Select all the 250 movies blocks from a single plage
        movie_blocks = html_soup.find_all('div', class_='lister-item mode-advanced')

        # Extract data from individual movie container
        for block in movie_blocks:

            # If the movie has Metascore, then extract:
            if (block.find('div', class_='ratings-metascore') is not None) and (
                    block.find('span', class_="certificate") is not None):
                # Create a dict() where all the attributes will be stored to be appended to the db list created above
                movie = {}

                # The name
                name = block.h3.a.text
                movie['name'] = name

                # The year
                year = block.find('span', class_='lister-item-year').text
                movie['year'] = year

                # IMDB Ratings
                rating = float(block.strong.text)
                movie['rating'] = rating

                # Metascore
                metascore = block.find('span', class_="metascore")
                metascore = int(metascore.text)
                movie['metascore'] = metascore

                # Votes
                votes = block.find('span', attrs={'name': 'nv'})
                votes = int(votes['data-value'])
                movie['votes'] = votes

                # Box Office
                box_office = list(block.find('p', class_='sort-num_votes-visible'))
                box_office = int(box_office[-2]['data-value'].replace(",", ""))
                movie['box_office'] = box_office

                # Duration
                duration = block.find('span', class_="runtime")
                duration = int(duration.text.split()[0])
                movie['duration'] = duration

                # Genre
                genre = block.find('span', class_="genre")
                genre = genre.text.strip().replace(" ", "").split(",")
                movie['genre'] = genre

                # Certification
                certification = block.find('span', class_="certificate")
                certification = certification.text
                movie['certification'] = certification

                # Get block for crew information
                crew = block.find_all('a')

                # Get director information
                director_name = list(crew)[-5].text
                director_link = crew[-5].attrs.get('href')
                director_country = get_birth_country(director_link)
                director_gender = get_gender(director_name)
                director_dict = {'name': director_name,
                                 'birth_country': director_country,
                                 'gender': director_gender
                                 }
                movie['director'] = director_dict

                # Get cast information
                cast = [a.text for a in list(crew)[-4:]]
                movie['cast'] = cast

                db_test.append(movie)

    return db_test


# Eliminate all movie entries where the birth country of the director is not composed of just letters
def clean_country(my_list):
    size = len(list(my_list))
    for count, movie in enumerate(my_list[::-1]):
        country = movie['director']['birth_country'].replace(" ", "")
        if not country.isalpha() or country == 'NA':
            del my_list[(size - 1) - count]


# Eliminate all movie entries where the birth country of the director is not 'Male'or 'Female'
def clean_gender(my_list):
    size = len(list(my_list))
    for count, movie in enumerate(my_list[::-1]):
        gender = movie['director']['gender']
        if gender == 'NA':
            del my_list[(size - 1) - count]


# Convert the year attribute for all movies to an int
def fix_year(my_list):
    import re

    if type(my_list['year']) != int:
        for movie in my_list[::-1]:
            year = movie['year']
            year = re.sub('[^0-9]', '', year)
            if isinstance(int(year), int):
                movie['year'] = int(year)

    return my_list




if __name__ == '__main__':
    # Retrieve data from imdb.com
    imdb_original = get_data(9000)

    # Create a deepcopy of the original dataset
    imdb_clean = copy.deepcopy(imdb_original)


    # Apply the fixes to the data
    clean_country(imdb_clean)
    clean_gender(imdb_clean)
    dataset_clean = fix_year(imdb_clean)

    # Creates a JSON file

    with open('imdb_genre.json', 'w') as file:
        json.dump(imdb_clean, file)

    # Create reference data for main.py
    IMDB_DATA = dataset_clean

    # Instead of using this object to create the web service a new .py file was created with the content of the JSON file
    # so the main.py doesn't rely in running this whole script
