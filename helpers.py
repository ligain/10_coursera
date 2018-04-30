import json
import re
from bs4 import BeautifulSoup
from datetime import datetime


def get_rating(course_instance_info):
    rating_aggr = course_instance_info.get('aggregateRating')
    rating_value = rating_aggr.get('ratingValue')
    if rating_value is not None:
        return float(rating_value)


def get_start_date(course_instance_info):
    start_date_str = course_instance_info.get('startDate')
    if start_date_str:
        return datetime.strptime(start_date_str, '%Y-%m-%d')


def get_languages(html_soup):
    lang_wrapper = html_soup.select('div.rc-Language').pop()
    if lang_wrapper:
        return re.split(r'\W+', lang_wrapper.text)[0]


def parse_course(course_url, course_html):
    html_soup = BeautifulSoup(course_html, 'html.parser')
    try:
        microdata = json.loads(html_soup.select(
            'script[type="application/ld+json"]').pop().text)
    except json.JSONDecodeError:
        microdata = {}

    title = microdata.get('name')

    languages = get_languages(html_soup)

    weeks = len(html_soup.select('div.week'))

    course_instance_info = microdata.get('hasCourseInstance')
    if course_instance_info:
        start_date = get_start_date(course_instance_info)
        avg_rating = get_rating(course_instance_info)
    else:
        start_date = None
        avg_rating = None

    return {
            'url': course_url,
            'title': title,
            'languages': languages,
            'start_date': start_date,
            'weeks': weeks,
            'avg_rating': avg_rating
        }
