import os

import numpy as np


def get_page_list():
    pages = []
    with open('site.txt') as f:
        pages = f.readlines()
        pages = remove_and_replace_element(pages)
    
    return pages

def page_split(raw_page):
    page = raw_page.split(',')[0]
    page = f'{page}.png'

    return page

def threshold_split(raw_page):
    try: 
        threshold = raw_page.split(',')[1]
    except:
        threshold = '0.01'

    return threshold

def remove_and_replace_element(pages):
    pages = [
        page.replace(
            'http://', ''
        ).replace(
            'https://', ''
        ).replace(
            '\n', ''
        ).replace(
            '/', '_'
        ) for page in pages
    ]

    return pages

def remove_prefix_and_suffix(contents):
    prefixes = (
        'Blink-Diff', 'Copyright', 'Clipping', 'Images', 'Wrote', 'Time', '---'
    )
    for content in contents[:]:
        if content.startswith(prefixes):
            contents.remove(content)

    suffixes = ('different')
    for content in contents[:]:
        if content.endswith(suffixes):
            contents.remove(content)

    return contents

def group_content(contents):
    contents_grouped = np.array(contents).reshape(len(contents)//3, 3)

    return contents_grouped

def report(content_grouped):
    for content in content_grouped:
        if content[2] == 'FAIL':
            fail_page = f'{content[0]} - {content[1]}'
            return fail_page

def generate_difference_report(page, threshold):
    fail_list = []

    os.system(f'./scripts/compare.sh {page} {threshold} > pages_compare_result.txt')   
    with open('pages_compare_result.txt') as f:
        contents = f.readlines()
        contents = remove_and_replace_element(contents)
        contents = remove_prefix_and_suffix(contents)
        contents_grouped = group_content(contents)
        fail_list = report(contents_grouped)

    return fail_list

def get_fail_list(pages):
    fail_list = []
    for raw_page in pages:
        print (raw_page)

        page = page_split(raw_page)
        threshold = threshold_split(raw_page)
        fail_list.append(generate_difference_report(page, threshold))
        
    return fail_list

def count_report(fail_list):
    fail_list_and_count = []

    count_all_page = len(fail_list)
    fail_list_and_count.append(count_all_page)

    fail_list = [page for page in fail_list if page is not None]
    count_fail_page = len(fail_list)
    fail_list_and_count.append(count_fail_page)

    fail_list_and_count.append(fail_list)

    return fail_list_and_count

def main_process():
    pages = get_page_list()
    fail_list = get_fail_list(pages)
    fail_list_and_count = count_report(fail_list)

    print('================ FAIL Pages ================')
    for page in fail_list_and_count [2]: 
        print(page)

    print(f'Fail: {fail_list_and_count[1]}/{fail_list_and_count[0]}')

    os.remove('pages_compare_result.txt')


if __name__ == '__main__':
    main_process()
