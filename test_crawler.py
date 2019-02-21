import requests
import unittest2
from crawler import get_gender, get_birth_country


class TestGetGender(unittest2.TestCase):
    def test_get_gender(self):
        # Test gender for Male and Female
        self.assertEqual(get_gender('Sean Penn'), 'Male')
        self.assertEqual(get_gender('Natalie Portman'), 'Female')

    def test_values(self):
        # Make sure vale erros are raised when necessary
        self.assertRaises(TypeError, get_gender, 2)
        self.assertRaises(TypeError, get_gender, -2.2)
        self.assertRaises(TypeError, get_gender, True)


class TestGetCountry(unittest2.TestCase):
    def test_values(self):
        # Make sure vale erros are raised when necessary
        self.assertRaises(TypeError, get_birth_country, 2)
        self.assertRaises(TypeError, get_birth_country, -2.2)
        self.assertRaises(TypeError, get_birth_country, True)


class TestLinks(unittest2.TestCase):
    def test_movie_link(self):
        start = str(251)
        url = 'https://www.imdb.com/search/title?title_type=feature&sort=boxoffice_gross_us,desc&count=250&start=' + \
              start + '&ref_=adv_nxt'
        response = requests.get(url, headers={"Accept-Language": "en-US, en;q=0.5"})
        self.assertEqual(404, response.status_code)

    def test_gender_link(self):
        name_string = '+'.join('Hugh Jackman'.split())
        url = 'https://www.imdb.com/search/name?name=' + name_string + '&gender=female'
        response = requests.get(url, headers={"Accept-Language": "en-US, en;q=0.5"})
        self.assertEqual(404, response.status_code)

    def test_country_link(self):
        link = '/name/nm0003506/?ref_=adv_li_dr_0'
        url = 'https://www.imdb.com' + link
        response = requests.get(url, headers={"Accept-Language": "en-US, en;q=0.5"})
        self.assertEqual(404, response.status_code)


if __name__ == '__main__':
    unittest2.main()
