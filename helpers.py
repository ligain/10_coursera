from bs4 import BeautifulSoup
from datetime import datetime, date


class CourseParser:

    def __init__(self, course_url, course_html):
        self.html_soup = BeautifulSoup(course_html, 'html.parser')
        self.url = course_url
        self.json = self.html_soup.select(
            'script.type="application/ld+json"').pop()

    def _get_title(self):
        title_text = self.html_soup.title.text
        return title_text.split('|')[0].strip() if title_text else ''

    def _get_languages(self):
        lang_wrapper = self.html_soup.select('div.rc-Language').pop()
        if not lang_wrapper:
            return []
        if lang_wrapper.strong is None:
            return [lang_wrapper.text]
        lang_wrapper.strong.decompose()
        langs_list = lang_wrapper.text.split(',')
        return langs_list

    def _get_start_date(self):
        start_wrapper = self.html_soup.select('div.startdate span').pop()
        if not start_wrapper:
            return
        current_year = str(date.today().year)
        date_string = start_wrapper.text.replace('Starts', current_year)
        return datetime.strptime(date_string, '%Y %b %d')

    def _get_length(self):
        return len(self.html_soup.select('div.week'))

    def _get_avg_rating(self):
        pass

    def get_properties(self):
        return {
            'url': self.url,
            'title': self._get_title(),
            'languages': self._get_languages(),
            'start_date': self._get_start_date(),
            'weeks': self._get_length()
        }
