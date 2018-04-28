import json

from bs4 import BeautifulSoup
from datetime import datetime, date


class CourseParser:

    def __init__(self, course_url, course_html):
        self.html_soup = BeautifulSoup(course_html, 'html.parser')
        self.url = course_url
        try:
            self.json = json.loads(self.html_soup.select(
                'script[type="application/ld+json"]').pop().text)
        except json.JSONDecodeError:
            self.json = {}

    def _get_title_html(self):
        title_text = self.html_soup.title.text
        title = title_text.split('|')[0].strip() if title_text else ''
        return title

    def _get_title_json(self):
        return self.json.get('name')

    def _get_languages_html(self):
        lang_wrapper = self.html_soup.select('div.rc-Language').pop()
        if not lang_wrapper:
            return []
        if lang_wrapper.strong is None:
            return [lang_wrapper.text]
        lang_wrapper.strong.decompose()
        langs_list = lang_wrapper.text.split(',')
        return langs_list

    def _get_start_date_html(self):
        start_wrapper = self.html_soup.select('div.startdate span').pop()
        if not start_wrapper:
            return
        current_year = str(date.today().year)
        date_string = start_wrapper.text.replace('Starts', current_year)
        try:
            start_date = datetime.strptime(date_string, '%Y %b %d')
        except ValueError:
            return
        return start_date

    def _get_start_date_json(self):
        course_instance_info = self.json.get('hasCourseInstance')
        if course_instance_info:
            start_date_str = course_instance_info.get('startDate')
            if not start_date_str:
                return
            return datetime.strptime(start_date_str, '%Y-%m-%d')

    def _get_length_html(self):
        return len(self.html_soup.select('div.week'))

    def _get_avg_rating_html(self):
        ratings_wrapper = self.html_soup.select(
            'div.ratings-info div.ratings-text span')
        if not ratings_wrapper:
            return
        rating, _ = ratings_wrapper[0].text.split()
        return float(rating)

    def _get_avg_rating_json(self):
        course_instance_info = self.json.get('hasCourseInstance')
        if course_instance_info:
            rating_aggr = course_instance_info.get('aggregateRating')
            rating_value = rating_aggr.get('ratingValue')
            if rating_value is None:
                return
            return float(rating_value)

    def _get_property(self, prop_name, methods):
        for method in methods:
            method_name = '_get_{}_{}'.format(prop_name, method)
            method_result = getattr(self, method_name)()
            if method_result:
                return method_result
            continue

    def get_properties(self):
        return {
            'url': self.url,
            'title': self._get_property('title', ['json', 'html']),
            'languages': self._get_property('languages', ['html']),
            'start_date': self._get_property('start_date', ['json', 'html']),
            'weeks': self._get_property('length', ['html']),
            'avg_rating': self._get_property('avg_rating', ['json', 'html'])
        }
