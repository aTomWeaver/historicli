import csv
import click
from termcolor import colored, cprint
from pprint import pprint
from operator import itemgetter
from matchers import COL_IDX, BC_MATCHERS, CIRCA_MATCHERS, CAT_MATCHERS

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

def chrono_sort(timeline_list):
    # sort bc items
    bc_list = [item for item in timeline_list if item[0] == 'BC']
    bc_list = sorted(bc_list, key=lambda row: int(row[2]), reverse=True)
    # sort ad items
    ad_list = [item for item in timeline_list if item[0] == 'AD']
    ad_list = sorted(ad_list, key=lambda row: int(row[2]))
    # join and return
    return bc_list + ad_list

def filter_timeline_list(by, matcher, timeline_list):
    '''returns a timeline_list that has been filtered from the given
    timeline_list by a given matcher
    '''
    search_index = COL_IDX[by]
    return [row for row in timeline_list if matcher in row[search_index]]

def get_timeline_list(source=TIMELINE_PATH):
    '''Reads the source file and returns a list of the rows as lists.
    Defaults to reading the main timeline path but can read a different
    csv for importing mass dates'''
    timeline_list = []
    with open(source, 'r', encoding='utf-8', newline='') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for row in reader:
            timeline_list.append(row)
    return timeline_list



def format_timeline_list(timeline_list):
    '''formats the passed timeline_list and returns the output'''
    def pad_year(year):
        '''pad year with left spaces until 4 chars long'''
        if len(year) < 4:
            while len(year) < 4:
                year = ' ' + year
        return year
    output = []
    for row in timeline_list:
        formatted_row = ''
        for index, item in enumerate(row):
            if index == 0:  # epoch
                formatted_row += colored(item, 'white', attrs=['dark', 'bold'])
            elif index == 1:  # circa
                formatted_row += colored(item, attrs=['bold'])
            elif index == 2:  # year
                formatted_row += colored(pad_year(item), attrs=['bold'])
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
        'year': input('Year: '),
        'category': input('Category: '),
        'description': input('Description: '),
        'tags': input('Tags (comma-separated): ').lower()
    }
    # get year (then format to ad or circa)
    # get category
    # get description
    # get any tags

def clean_input(input):
    '''cleans up user input and returns a row;
    this function is really ugly- refactor
    '''
    user_row = []
    epoch, circa = ('', '')
    year, category, description, tags = input.values()
    year = str(year)
    category = category.lower()
    for matcher in BC_MATCHERS:
        if matcher in year:
            epoch = 'BC'
            year = year.replace(matcher, '')
            break
        else:
            epoch = 'AD'
    user_row.append(epoch)
    for matcher in CIRCA_MATCHERS:
        if matcher in year:
            circa = r'~'
            year = year.replace(matcher, '')
            break
        else:
            circa = ' '
    user_row.append(circa)
    user_row.append(year.strip())
    for matcher in CAT_MATCHERS.keys():
        if matcher.lower() in category:
            category = CAT_MATCHERS[matcher]
            break
    user_row.append(category)
    user_row.append(description.strip())
    user_row.append(tags)
    return user_row
    
@click.command()
# @click.argument()
def print_timeline(timeline_list=get_timeline_list()):
    output = format_timeline_list(chrono_sort(timeline_list))
    for row in output:
        click.echo(row)


# @click.command()
@click.option('-p', '--person',)
def cli_echo():
    pass

if __name__ == '__main__':
    print_timeline()
