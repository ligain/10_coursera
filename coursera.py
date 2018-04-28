import os
from lxml import etree
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

from helpers import CourseParser


FEED_URL = 'https://www.coursera.org/sitemap~www~courses.xml'


def get_courses(url, count=20):
    feed = requests.get(url)
    if not feed.ok:
        return []

    feed_tree = etree.fromstring(feed.text.encode())
    default_namespace = feed_tree.nsmap.get(None)
    loc_tag = '{{{ns}}}loc'.format(ns=default_namespace)

    for _, element in etree.iterwalk(feed_tree, tag=loc_tag):
        if count > 0:
            count -= 1
            course_url = element.text
            yield course_url


def parse_courses(courses_responses):
    for course_resp in courses_responses:
        if not course_resp.ok:
            continue
        yield CourseParser(course_url=course_resp.url,
                           course_html=course_resp.text).get_properties()


def get_courses_info(course_urls):
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        futures = {executor.submit(requests.get, url): url
                   for url in course_urls}

        for future in as_completed(futures):
            course_response = future.result()
            yield course_response


def save_courses_info_to_xlsx(filepath):
    pass


def get_args():
    pass


if __name__ == '__main__':

    courses_urls = get_courses(FEED_URL)

    courses_info = get_courses_info(courses_urls)

    courses_properties = parse_courses(courses_info)

    for course in courses_properties:
        print(course)
        break
    # print(list(courses_info))
