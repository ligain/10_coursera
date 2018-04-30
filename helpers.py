import json
import re
from bs4 import BeautifulSoup
from datetime import datetime


def parse_course(course_url, course_html):
    html_soup = BeautifulSoup(course_html, 'html.parser')
    try:
        microdata = json.loads(html_soup.select(
            'script[type="application/ld+json"]').pop().text)
    except json.JSONDecodeError:
        microdata = {}

    title = microdata.get('name')

    lang_wrapper = html_soup.select('div.rc-Language').pop()
    if not lang_wrapper:
        return
    languages = re.split(r'\W+', lang_wrapper.text)[0]

    weeks = len(html_soup.select('div.week'))

    course_instance_info = microdata.get('hasCourseInstance')
    if course_instance_info:

        rating_aggr = course_instance_info.get('aggregateRating')
        rating_value = rating_aggr.get('ratingValue')
        if rating_value is None:
            avg_rating = None
        else:
            avg_rating = float(rating_value)

        start_date_str = course_instance_info.get('startDate')
        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        else:
            start_date = None
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
