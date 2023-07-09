import csv
import click
from termcolor import colored, cprint
from pprint import pprint
from operator import itemgetter

TIMELINE_PATH = '/home/tom/code/python/history_timeline/historicli/timeline.csv'
COLORS = {
    'P': ('black', 'on_white', None),
    'E': ('black', 'on_yellow', 'yellow'),
    'M': ('black', 'on_blue', 'blue'),
    'B': ('black', 'on_cyan', 'cyan'),
    'A': ('black', 'on_red', 'red'),
    'L': ('black', 'on_magenta', 'magenta'),
    'S': ('black', 'on_green', 'green')
}
COL_IDX = {
    'epoch': 0,
    'circa': 1,
    'year': 2,
    'category': 3,
    'description': 4
}

def chrono_sort(timeline_list):
    return sorted(timeline_list, key=lambda row: row[2])

def filter_timeline_list(by, matcher, timeline_list):
    '''returns a timeline_list that has been filtered from the given
    timeline_list by a given matcher
    '''
    search_index = COL_IDX[by]
    return [row for row in timeline_list if matcher in row[search_index]]

def get_timeline_list():
    '''Reads the timeline.csv and returns a list of the rows as lists'''
    timeline_list = []
    with open(TIMELINE_PATH, 'r', encoding='utf-8', newline='') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for row in reader:
            timeline_list.append(row)
    return timeline_list


def format_timeline_list(timeline_list):
    '''formats the passed timeline_list and returns the output'''
    output = []
    for row in timeline_list:
        formatted_row = ''
        for index, item in enumerate(row):
            if index == 0:  # epoch
                formatted_row += colored(item, 'white', attrs=['dark', 'bold'])
            elif index < 3:  # circa & year
                formatted_row += colored(item, attrs=['bold'])
            elif index == 3:  # category
                cat_color, highlight, _ = COLORS[item]
                formatted_row += ' ' + \
                    colored(f' {item} ', cat_color, highlight)
            elif index == 4:  # description
                _, _, desc_color = COLORS[row[3]]
                formatted_row += ' ' + colored(item, desc_color)
        output.append(formatted_row)
    return output


def append_row(row):
    '''accepts an already cleaned row and appends it to the timeline.csv'''
    with open(TIMELINE_PATH, 'a', newline='') as timelinecsv:
        writer = csv.writer(timelinecsv, delimiter=',')
        writer.writerow(row)


def get_new_row_from_user():
    return {
        'year': int(input('Year: ')),
        'category': input('Category: '),
        'description': input('Description: '),
        'tags': input('Tags (comma-separated): ').lower()
    }
    # get year (then format to ad or circa)
    # get category
    # get description
    # get any tags


def print_timeline():
    output = format_timeline_list(get_timeline_list())
    for row in output:
        print(row)

user_row = get_new_row_from_user()
print(user_row)
# pprint(chrono_sort(filter_timeline_list('description', 'Bean', get_timeline_list())))
# pprint(get_timeline_list())
# append_row(['AD', '~', '1997', 'E', 'Ocarina of Time is released'])
