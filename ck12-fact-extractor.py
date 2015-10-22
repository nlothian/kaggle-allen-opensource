from __future__ import unicode_literals, print_function, division
from ebooklib import epub
import ebooklib
from bs4 import BeautifulSoup
import re
import os

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)

def normalize_text(text):
    return re.sub("\s+|\n", " ", text.strip());


def find_fact_list(soup):
    summary_points = []

    # some books use <h2>Lesson Summary</h2>
    h2s = soup.find_all(['h2'])
    for element in h2s:
        if "Lesson Summary" == element.get_text().strip():
            lst =  element.find_next_sibling("ul")
            children = lst.find_all(['li'])
            for child in children:
                summary_points.append(normalize_text(child.get_text().strip()))

    # some books use <p><strong>Key Concepts</strong></p>
    strongs = soup.find_all(['strong'])
    for element in strongs:
        if "Key Concepts" == element.get_text().strip():
            lst = element.parent.find_next_sibling("ul")
            children = lst.find_all(['li'])
            for child in children:
                summary_points.append(normalize_text(child.get_text().strip()))


    return summary_points


def get_lesson_summary(epub_item):
    soup = BeautifulSoup(item.content, 'html.parser')

    facts = find_fact_list(soup)
    for fact in facts:
        print(fact)

for file in os.listdir("./books"):
    if file.endswith(".epub"):
        book = epub.read_epub("./books/" + file)

        for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
            get_lesson_summary(item)
