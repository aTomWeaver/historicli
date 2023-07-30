import csv
import click
from termcolor import colored
import colored_traceback
# from termcolor import cprint
from pprint import pprint
# from operator import itemgetter
from matchers import COL_IDX, BC_MATCHERS, CIRCA_MATCHERS, CAT_MATCHERS

colored_traceback.add_hook()

TIMELINE_PATH = ('/home/tom/code/python/history_timeline/historicli/'
                 'timeline.csv')

COLORS = {
    'P': ('black', 'on_white', None),
    'E': ('black', 'on_yellow', 'yellow'),
    'M': ('black', 'on_blue', 'blue'),
    'B': ('black', 'on_cyan', 'cyan'),
    'A': ('black', 'on_red', 'red'),
    'L': ('black', 'on_magenta', 'magenta'),
    'S': ('black', 'on_green', 'green')
}


# increase efficiency by not grabbing the whole file every time
def get_timeline_list(source=TIMELINE_PATH):
    '''Reads the source file and returns a list of the rows as lists.
    Defaults to reading the main timeline path but can read a different
    csv for importing mass dates'''
    with open(source, 'r', encoding='utf-8', newline='') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        timeline_list = [row for row in reader]
    return timeline_list


def chrono_sort(timeline_list):
    return sorted(
            timeline_list,
            key=lambda row: int(row[0])
            )


def filter_timeline_list(by, matcher, timeline_list):
    '''returns a timeline_list that has been filtered from the given
    timeline_list by a given matcher
    '''
    search_index = COL_IDX[by]
    return [row for row in timeline_list if matcher in row[search_index]]


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

        # Epoch
        if int(row[0]) < 0:
            formatted_row += 'BC' + ' '
            row[0] = row[0][1:]  # drop the '-'
        else:
            formatted_row += 'AD' + ' '

        for index, item in enumerate(row):
            # Circa
            if index == 1:
                if item:
                    formatted_row += colored(item, attrs=['bold'])
                else:
                    formatted_row += ' '
            # Year
                formatted_row += colored(
                        pad_year(row[index-1]),
                        attrs=['bold']
                        )
            # Category
            elif index == 2:
                cat_color, highlight, _ = COLORS[item]
                formatted_row += ' ' + \
                    colored(f' {item} ', cat_color, highlight)

            # Description
            elif index == 3:
                _, _, desc_color = COLORS[row[2]]
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
@click.argument('start_year', default='1000000bc')
@click.option('-e', '--end-year', type=str)
@click.option('-c', '--category', type=str)
def print_timeline(start_year, end_year, category):
    timeline_list = get_timeline_list()

    # if start_year:
    for matcher in BC_MATCHERS:
        if matcher in start_year:
            start_year = '-' + start_year.replace(matcher, '').strip()
            break
    timeline_list = [row for row in timeline_list
                     if int(row[0]) >= int(start_year)]

    if end_year:
        for matcher in BC_MATCHERS:
            if matcher in end_year:
                end_year = '-' + end_year.replace(matcher, '').strip()
                break
        timeline_list = [row for row in timeline_list
                         if int(row[0]) < int(end_year)]

    if category:
        for matcher, cat in CAT_MATCHERS.items():
            if category.lower().strip() == matcher:
                category = cat
                break
        timeline_list = filter_timeline_list('category', category,
                                             timeline_list)

    output = format_timeline_list(chrono_sort(timeline_list))
    for row in output:
        click.echo(row)


if __name__ == '__main__':
    print_timeline()
