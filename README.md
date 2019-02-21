# IMDB Movie List

The goal of this project is to develop a Web Crawler in Python that returns a list of at least 5000 titles from https://www.imdb.com without the aid of any scrapping or matemathical frameworks (Scrapy/Selenium, Numpy/Pandas) and create a web service that returns the dataset using Flask or Tornado to answer the following questions:

* What is the probability that the director of a movie is Female?
* What is the average duration of the movies in the list?
* What is the probability of each movie in its genre to have a rating above 8?
* What is the probability of a movie to have a rating above 8 considering that the director is not American?

Additionally, the development of the Python code must include a Unit Test and a DockerFile


## Web Crawler development

The first challenge was to develop a scrapping tool that would enable us to collect all the information needed to create the movie dataset. As IMDB does not have a proper API, it was necessary to read the text straight out of the URL request and filter the html code in order to retrieve the data we wanted. The attributes selected were:

* **name**: Movie title
* **year**: Release year
* **rating**: IMDB rating
* **metascore**: Metascore rating
* **votes**: Number of people that rated the movie
* **box_office**: US box office performance
* **duration**: length of the movie
* **genre**: List of film genres that describe the movie
* **certification**: Motion picture content rating system label
* **director**: Contains name, gender and birth place of the movie director
* **cast**: Contains a list with the name of the 4 biggest stars of the movie

Because of our inability to use a DataFrame, the format selected to build the dataset was a list of dictionaries  where each element of the list is a movie, and each movie is a dictionary containing all the attributes listed above as it can be seen below: 

```python
{'name': 'Star Wars: Episode VII - The Force Awakens',
 'year': '(2015)',
 'rating': 8.0,
 'metascore': 81,
 'votes': 771951,
 'box_office': 936662225,
 'duration': 136,
 'certification': 'PG-13',
 'director': {'name': 'J.J. Abrams', 'birth_country': 'USA', 'gender': 'Male'},
 'cast': ['Daisy Ridley', 'John Boyega', 'Oscar Isaac', 'Domhnall Gleeson']}
```

After the website was scrapped and the dataset was populated with 5084 movies, we created a google web service that stored the dataset in the cloud and used it to calculate the statistics that were requested.

## Answers:

### Load dataset from web service
```python
import requests
import json

url = 'https://imdb-232317.appspot.com/'
response = requests.get(url)
imdb = json.loads(response.text)
```

### 1. What is the probability that the director of a movie is Female?
```python
# Count the 
def count_director_attr(mylist):
    count = 0
    for movie in imdb:
        if movie['director']['gender'] == 'Female':
            count += 1
    
    return count

fem_count = count_director_attr(imdb)
fem_prob = fem_count / len(imdb)

print ("{0:.2%}".format(fem_prob))
```
**10.15%**

### 2. What is the average duration of the movies in the list?

```python
def avg_duration(mylist):
    total_minutes = 0
    for movie in imdb:
       total_minutes += movie['duration']
    
    return total_minutes / len(imdb)

print (round(avg_duration(imdb)), 'minutes')
```
**110 minutes**

### 3. What is the probability of each movie in its gender to have a rating above 8?
First, we created a genre histogram for all movies. Then we filtered the all the movies with a rating above 8 and created another histogram with the filtered data. Finally we compared the two histograms and took the percentages.
```python
# Histogram movies 
def genre_hist(mylist):
    genres = {}
    for movie in mylist:
        for genre in movie['genre']:
            genres[genre] = genres.get(genre, 0) + 1
    
    return genres

genre_hist_all = genre_hist(imdb)
print(genre_hist_all)
```
```python
{'Action': 1123,
 'Adventure': 928,
 'Fantasy': 393,
 'Sci-Fi': 351,
 'Drama': 2898,
 'Romance': 1007,
 'Animation': 200,
 'Crime': 944,
 'Family': 305,
 'Thriller': 751,
 'Comedy': 1984,
 'Biography': 401,
 'Mystery': 438,
 'Horror': 454,
 'Sport': 134,
 'War': 99,
 'Music': 194,
 'History': 177,
 'Musical': 59,
 'Western': 38,
 'Film-Noir': 5}
```


```python
# Filter movies above a certain rating
def rating_above(mylist, rating):
    new_list = []
    for movie in mylist:
        if movie['rating'] > rating:
            new_list.append(movie)
    
    return new_list        

imdb_8 = rating_above(imdb, 8)

print("There are", len(imdb_8), 'movies with rating above 8')
```
187 movies with rating above 8

```python
# Create hist for filtered data
genre_hist_8 = genre_hist(imdb_8)
print(genre_hist_8)
```
```python
{'Action': 25,
 'Adventure': 46,
 'Fantasy': 16,
 'Sci-Fi': 18,
 'Crime': 34,
 'Drama': 133,
 'Thriller': 31,
 'Animation': 15,
 'Comedy': 29,
 'Romance': 18,
 'Mystery': 20,
 'Family': 5,
 'War': 11,
 'Biography': 22,
 'Music': 4,
 'History': 10,
 'Western': 6,
 'Sport': 4,
 'Horror': 4,
 'Musical': 1}
```
Please note that the same movie may be counted in my than one genre so that's the reason there are more than 187 counts in the histogram.

```python
# Get probabilities
def percent(hist_n, hist_all):
    new_hist ={}
    for genre in hist_all:
        new_hist[genre] = hist_n.get(genre, 0) / hist_all.get(genre, 0)
    
    return new_hist


new_hist = percent(genre_hist_8, genre_hist_all)

for genre in new_hist:
    print(genre + ': ' + "{0:.2%}".format(new_hist[genre]))
```

```python
Action: 2.23%
Adventure: 4.96%
Fantasy: 4.07%
Sci-Fi: 5.13%
Drama: 4.59%
Romance: 1.79%
Animation: 7.50%
Crime: 3.60%
Family: 1.64%
Thriller: 4.13%
Comedy: 1.46%
Biography: 5.49%
Mystery: 4.57%
Horror: 0.88%
Sport: 2.99%
War: 11.11%
Music: 2.06%
History: 5.65%
Musical: 1.69%
Western: 15.79%
Film-Noir: 0.00%
```

#### 4. What is the probability of a movie to have a rating above 8 considering that the director is not american?
```python
# Filter by nationality
def not_national(mylist, nationality):
    new_list = []
    for movie in mylist:
        if movie['director']['birth_country'] != nationality:
            new_list.append(movie)
    return new_list

imdb_8_not_USA = not_national(imdb_8, 'USA')
result = len(imdb_8_not_USA) / len(imdb)

print("{0:.2%}".format(result))
```
**1.89%**