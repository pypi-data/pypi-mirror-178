import json
import re
import sys

import pendulum
import requests
from bs4 import BeautifulSoup

ABB_URL = 'http://audiobookbay.fi'


def get_url(page_num):
    u = ABB_URL.rstrip('/') + '/'
    if page_num > 1:
        u = f'{u}page/{page_num}/'
    return u


def abb_post_to_dict(html):
    post = BeautifulSoup(str(html), 'html.parser')
    url = post.find('div', class_='postTitle').find('a').get('href')
    post_title = post.find('div', class_='postTitle').get_text(strip=True)
    image_url = post.find('img').get('src')

    def extract_elem(match_str):
        elem = post.find(string=re.compile(match_str))
        if elem:
            elem = elem.extract()
            return elem.get_text().replace(match_str, '')

    post_date_str = extract_elem('Posted:').strip()
    post_date = pendulum.from_format(post_date_str, 'D MMM YYYY').to_date_string()

    category_str = extract_elem('Category:')
    if category_str:
        elem_list = category_str.split('\xa0')
        elem_list = [s.strip() for s in elem_list]
        elem_list = [s for s in elem_list if s]
        category_str = json.dumps(elem_list)

    keywords_str = extract_elem('Keywords:')
    if keywords_str:
        elem_list = keywords_str.split('\xa0')
        elem_list = [s.strip() for s in elem_list]
        elem_list = [s for s in elem_list if s]
        keywords_str = json.dumps(elem_list)

    language = extract_elem('Language:')
    if language:
        language = language.strip()

    [s.unwrap() for s in post.find_all('span')]
    post.smooth()
    file_format = extract_elem('Format:')
    if file_format and '/' in file_format:
        file_format = file_format.split('/')[0].strip()

    return {
        'url': url,
        'post_title': post_title,
        'post_date': post_date,
        'image_url': image_url,
        'best_image': image_url,
        'file_format': file_format,
        'category_str': category_str,
        'keywords_str': keywords_str,
        'language': language,
    }


class Abb:
    session = requests.session()

    def __init__(self):
        self.posts_by_page = []

    def __len__(self):
        return len(self.posts_by_page)

    @property
    def all_posts(self):
        posts = []
        for page in self.posts_by_page:
            posts.extend(page['posts'])
        return posts

    @property
    def min_post_date(self):
        dts = [b.get('post_date') for b in self.all_posts if b.get('post_date')]
        if dts:
            return pendulum.parse(min(dts))

    def read_page(self, page_num):
        url = get_url(page_num)
        try:
            resp = self.session.get(url, timeout=5.0)
        except requests.RequestException as err:
            print(f"Error page {page_num} {url}")
            # print(str(err))
            return []

        soup = BeautifulSoup(resp.text, 'html.parser')

        posts = soup.find_all('div', class_='post')
        posts = [p for p in posts if p.find('div', class_='postTitle')]
        page_result = [abb_post_to_dict(post) for post in posts]

        self.posts_by_page.append(dict(page=page_num, posts=page_result))

        return page_result


def read_pages(start_page, end_page):
    abb = Abb()
    for p in range(start_page, end_page + 1):
        abb.read_page(p)

    return abb.all_posts


def main() -> None:
    """Read the Real Python article feed."""
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    opts = [o for o in sys.argv[1:] if o.startswith("-")]

    if len(args) > 1:
        start = int(args[0])
        end = int(args[1])
    elif len(args) == 1:
        start = 1
        end = int(args[0]) + 1
    else:
        start, end = 1, 5
    """
    # Show help message
    if "-h" in opts or "--help" in opts:
        viewer.show(__doc__)
        raise SystemExit()

    # Should links be shown in the text
    show_links = "-l" in opts or "--show-links" in opts

    # Get URL from config file
    url = reader.URL

    # An article ID is given, show article
    if args:
        for article_id in args:
            article = feed.get_article(article_id, links=show_links, url=url)
            viewer.show(article)

    # No ID is given, show list of articles
    else:
        site = feed.get_site(url=url)
        titles = feed.get_titles(url=url)
        viewer.show_list(site, titles)"""


if __name__ == "__main__":
    main()
