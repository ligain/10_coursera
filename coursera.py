import argparse
import os
from lxml import etree
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from helpers import parse_course
from openpyxl import Workbook


FEED_URL = 'https://www.coursera.org/sitemap~www~courses.xml'


def get_courses_urls(url, count=20):
    feed = requests.get(url)
    if not feed.ok:
        return []

    feed_tree = etree.fromstring(feed.text.encode())
    default_namespace = feed_tree.nsmap.get(None)
    loc_tag = '{{{ns}}}loc'.format(ns=default_namespace)
    elements = iter(etree.iterwalk(feed_tree, tag=loc_tag))

    while count > 0:
        _, element = next(elements)
        course_url = element.text
        count -= 1
        yield course_url


def parse_courses(courses_responses):
    for course_resp in courses_responses:
        if not course_resp.ok:
            continue
        yield parse_course(course_resp.url, course_resp.text)


def get_courses_info(course_urls):
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        futures = {executor.submit(requests.get, url): url
                   for url in course_urls}

        for future in as_completed(futures):
            course_response = future.result()
            yield course_response


def prepare_course(course_dict):
    return [
        course_dict['url'],
        course_dict['title'],
        course_dict['languages'],
        course_dict['start_date'].isoformat() if course_dict.get('start_date') else None,
        course_dict['weeks'],
        course_dict['avg_rating']
    ]


def get_courses_workbook(courses):
    workbook = Workbook(write_only=True)
    workbook_sheet = workbook.create_sheet(title='Courses')
    headers = ['Url', 'Title', 'Languages', 'Start date',
               'Weeks', 'Average rating']
    workbook_sheet.append(headers)
    for course in courses:
        prepared_row = prepare_course(course)
        workbook_sheet.append(prepared_row)
    return workbook


def is_path(path):
    if not os.path.exists(path):
        raise argparse.ArgumentTypeError(
            'It should be valid path'
        )
    return path


def get_args():
    parser = argparse.ArgumentParser(
        description='A tool to get info about courses on coursera.org '
                    'and to save them in a xlsx file'
    )
    parser.add_argument(
        '-p', '--path',
        help='Path where a xlsx file should be saved',
        type=is_path,
        default='.',
    )
    parser.add_argument(
        '-f', '--filename',
        help='Name of a xlsx file with courses info',
        default='courses.xlsx'
    )
    return parser.parse_args()


if __name__ == '__main__':

    args = get_args()
    output_file_path = os.path.join(args.path, args.filename)

    courses_urls = get_courses_urls(FEED_URL)

    courses_info = get_courses_info(courses_urls)

    courses_properties = parse_courses(courses_info)

    workbook = get_courses_workbook(courses_properties)

    workbook.save(output_file_path)
