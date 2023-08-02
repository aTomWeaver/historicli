import csv
import click
from termcolor import colored
import colored_traceback
# from termcolor import cprint
# from operator import itemgetter
from matchers import COL_IDX, BC_MATCHERS, CIRCA_MATCHERS, CAT_MATCHERS

colored_traceback.add_hook()

TIMELINE_PATH = ('/home/tom/code/python/history_timeline/hs/'
                 'timeline.csv')

PERIODS_PATH = ('/home/tom/code/python/history_timeline/hs/'
                'periods.csv')

COLORS = {
    'P': ('black', 'on_white', None),
    'E': ('black', 'on_yellow', 'yellow'),
    'M': ('black', 'on_blue', 'blue'),
    'B': ('black', 'on_cyan', 'cyan'),
    'A': ('black', 'on_red', 'red'),
    'L': ('black', 'on_magenta', 'magenta'),
    'S': ('black', 'on_green', 'green')
}


def get_timeline_list(source=TIMELINE_PATH):
    '''Reads the source file and returns a list of the rows as lists.
    Defaults to reading the main timeline path but can read a different
    csv for importing mass dates'''
    with open(source, 'r', encoding='utf-8', newline='') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        timeline_list = [row for row in reader]
    return timeline_list


def append_row_to_timeline(cleaned_row):
    '''accepts an already cleaned row and appends it to the timeline.csv'''
    with open(TIMELINE_PATH, 'a', newline='') as timelinecsv:
        writer = csv.writer(timelinecsv, delimiter=',')
        writer.writerow(cleaned_row)


def append_row_to_periods(cleaned_row):
    '''accepts an already cleaned row and appends it to the periods.csv'''
    with open(PERIODS_PATH, 'a', newline='') as periodscsv:
        writer = csv.writer(periodscsv, delimiter=',')
        writer.writerow(cleaned_row)
    pass


def sort_timeline_list(timeline_list):
    sorted_timeline = sorted(timeline_list, key=lambda row: int(row[0]))
    # with open(TIMELINE_PATH, 'w', encoding='utf-8', newline='') as csv_file:
    #     writer = csv.writer(csv_file, delimiter=',')
    #     writer.writerows(sorted_timeline)
    return sorted_timeline


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
                formatted_row += colored(pad_year(row[index-1]),
                                         attrs=['bold'])
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


def get_new_row_from_user():
    return {
        'year': input('Year: '),
        'category': input('Category: '),
        'description': input('Description: '),
        'tags': input('Tags (comma-separated): ').lower()
    }


def clean_timeline_input(input):
    '''
    Cleans up user input and returns a row.
    This function is really ugly- refactor.
    '''
    user_row = []
    circa = ''
    year, category, description, tags = input.values()

    if not tags:
        tags = 'none'
    year = str(year)
    category = category.lower()

    for matcher in BC_MATCHERS:
        if matcher in year:
            year = '-' + year.replace(matcher, '')
            break
    year = year.strip()

    for matcher in CIRCA_MATCHERS:
        if matcher in year:
            circa = r'~'
            year = year.replace(matcher, '')
            break
        else:
            circa = ''

    for matcher in CAT_MATCHERS.keys():
        if matcher.lower() in category:
            category = CAT_MATCHERS[matcher]
            break

    user_row.append(year)
    user_row.append(circa)
    user_row.append(category)
    user_row.append(description.strip())
    user_row.append(tags)
    return user_row


def convert_bc(year):
    for matcher in BC_MATCHERS:
        if matcher in year:
            year = '-' + year.replace(matcher, '')
            break
        year = year.strip()
    return year


def get_period_range(title):
    with open(PERIODS_PATH, 'r', newline='') as periodscsv:
        reader = csv.reader(periodscsv, delimiter=',')
        # get a list of periods with the search term partially in title col
        periods = [row for row in reader if title in row[2]]
        for row in periods:
            # convert the title col of the row into a list
            row_with_title_list = [row[0], row[1], row[2].split(',')]
            # search until an exact match of title is found in title col
            for row_title in row_with_title_list[2]:
                row_title = row_title.strip()
                if title == row_title:
                    # return the whole row it was found in
                    start_year, end_year, _ = row
                    return (row[0], row[1])


@click.group()
def cli():
    pass


@cli.group()
def add():
    pass


@add.command()
def prompt():
    append_row_to_timeline(clean_timeline_input(get_new_row_from_user()))


@add.command()
@click.argument('year', required=True, type=str)
@click.argument('category', required=True, type=str)
@click.argument('description', required=True, type=str)
@click.argument('tags', required=False, type=str)
def manual(year, category, description, tags):
    input = {
            "year": year,
            "category": year,
            "description": description,
            "tags": tags
            }
    append_row_to_timeline(clean_timeline_input(input))


@add.command()
@click.argument('start_year', required=True, type=str)
@click.argument('end_year', required=True, type=str)
@click.argument('title', required=True, type=str)
def period(start_year, end_year, title):
    start_year = convert_bc(start_year)
    end_year = convert_bc(end_year)
    append_row_to_periods([start_year, end_year, title])


@cli.command()
@click.argument('start_year', default='1000000bc')
@click.option('-e', '--end-year', type=str,
              help='Get only results up to end year.')
@click.option('-c', '--category', type=str,
              help='Get only results in a given category.')
@click.option('-g', '--grep', type=str,
              help='Get only results containing given string.')
@click.option('-p', '--period', type=str,
              help='Get only results that fall in a given named time period.')
def ls(start_year, end_year, category, grep, period):
    '''
    Prints the timeline with given parameters.
    end_year is INCLUSIVE
    '''
    timeline_list = get_timeline_list()

    if period:
        print(f'period: {period}')
        start_year, end_year = get_period_range(period.strip())

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
                         if int(row[0]) <= int(end_year)]

    if category:
        for matcher, cat in CAT_MATCHERS.items():
            if category.lower().strip() == matcher:
                category = cat
                break
        timeline_list = filter_timeline_list('category', category,
                                             timeline_list)

    if grep:
        timeline_list = [row for row in timeline_list
                         if grep in row[3]+row[4]]

    output = format_timeline_list(sort_timeline_list(timeline_list))
    for row in output:
        click.echo(row)


if __name__ == '__main__':
    cli()
