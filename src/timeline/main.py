from pprint import pprint
import csv
import os
import click
from termcolor import colored
import colored_traceback
# from termcolor import cprint
# from operator import itemgetter
from matchers import COL_IDX, BC_MATCHERS, CIRCA_MATCHERS, CAT_MATCHERS

# colored_traceback for debugging
colored_traceback.add_hook()

# PATHS
root_dir = os.path.join('/', 'home', 'tom', 'code', 'python',
                        'history_timeline', 'src', 'timeline')
PATHS = {
        "timeline": os.path.join(root_dir, 'timeline.csv'),
        "periods": os.path.join(root_dir, 'periods.csv'),
        "groups": os.path.join(root_dir, 'groups.csv'),
        }

COLORS = {
    'P': ('black', 'on_white', None),
    'E': ('black', 'on_yellow', 'yellow'),
    'M': ('black', 'on_blue', 'blue'),
    'B': ('black', 'on_cyan', 'cyan'),
    'A': ('black', 'on_red', 'red'),
    'L': ('black', 'on_magenta', 'magenta'),
    'S': ('black', 'on_green', 'green')
}


def list_(source):
    '''Reads the periods file and returns a list of the rows as lists.'''
    if source not in PATHS:
        print('ERROR: Invalid source given.')
        return

    with open(PATHS[source], 'r', encoding='utf-8', newline='') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        next(reader, None)  # Skip the header row
        target_list = [row for row in reader]
    return target_list


def append_row(row, target):
    '''accepts an already cleaned row and appends it to the target csv'''
    if target not in PATHS:
        print(f'Invalid target. Cannot append to {target}')
        return

    with open(PATHS[target], 'a', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(row)


def pad_year(year):
    '''pad year with left spaces until 4 chars long'''
    if len(year) < 4:
        while len(year) < 4:
            year = ' ' + year
    return year


def sort_timeline_list(timeline_list):
    sorted_timeline = sorted(timeline_list, key=lambda row: int(row[0]))
    return sorted_timeline


def filter_timeline_list(by, matcher, timeline_list):
    '''returns a timeline_list that has been filtered from the given
    timeline_list by a given matcher
    '''
    search_index = COL_IDX[by]
    return [row for row in timeline_list if matcher in row[search_index]]


def format_timeline_list(timeline_list):
    '''formats the passed timeline_list and returns the output'''
    formatted_list = []
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
        formatted_list.append(formatted_row)
    return formatted_list


def format_period_list(period_list):
    formatted_list = []
    period_list = sort_timeline_list(period_list)
    for row in period_list:
        formatted_row = ''

        for index, year in enumerate((row[0], row[1])):
            if int(year) < 0:
                year = colored(pad_year(year[1:]) + ' BC', 'yellow')
            else:
                year = colored(pad_year(year), 'red')
            if index == 0:
                year += ' - '
            formatted_row += year

        period = colored(row[2], 'blue', attrs=['bold'])
        formatted_row += f'\n\t{period}\n'
        formatted_list.append(formatted_row)
    return formatted_list


def get_new_row_from_user():
    # TODO: reject invalid inputs
    # if 'birth, born, death, died, dies' in desc add relevant tag
    return {
        'year': input('Year: '),
        'category': input('Category: ').lower(),
        'description': input('Description: '),
        'tags': input('Tags (comma-separated): ').lower()
    }


def convert_bc_to_neg(year):
    for matcher in BC_MATCHERS:
        if matcher in year:
            year = '-' + year.replace(matcher, '')
            break
    return year


def clean_timeline_input(input):
    '''
    Cleans up user input and returns a row.
    This function is really ugly- refactor.
    '''
    user_row = []
    circa = ''
    year, category, description, tags = input.values()

    year = str(year)

    # Clean circa
    for matcher in CIRCA_MATCHERS:
        if matcher in year:
            circa = r'~'
            year = year.replace(matcher, '')
            break
        else:
            circa = ''

    # Clean year
    year = convert_bc_to_neg(year).strip()

    # Clean category
    category = category.lower()
    for matcher in CAT_MATCHERS.keys():
        if matcher.lower() in category:
            category = CAT_MATCHERS[matcher]
            break

    # Clean description
    description = description.strip()

    # Clean tags
    if not tags:
        tags = ''
    death_matchers = ['dies', 'died']
    birth_matchers = ['is born', 'was born', 'birth']
    for matcher in death_matchers:
        if matcher in description:
            if tags.strip() == '':
                tags += 'death'
            else:
                tags += ', death'
    for matcher in birth_matchers:
        if matcher in description:
            if tags.strip() == '':
                tags += 'birth'
            else:
                tags += ', birth'
    tags = tags.lower()

    user_row.extend([year, circa, category, description, tags])
    return user_row


def get_period_range(title):
    with open(PATHS['periods'], 'r', newline='') as periodscsv:
        reader = csv.reader(periodscsv, delimiter=',')
        next(reader, None)
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


######################################################################
# CLI ################################################################
######################################################################


def confirm_yes_no(message, yes_action, no_action):
    '''Prompts the user with a given message and calls one of two
    passed functions depending on the answer.
    '''
    confirmation = input(message + ' (y/n): ').lower()
    if confirmation == 'y' or confirmation == 'yes':
        yes_action()
    else:
        no_action()


@click.group()
def cli():
    pass


@cli.command()
@click.option('-m', '--manual', type=str, help='Accepts a single '
              'comma-delimited string with year, category, description, '
              'and n number of tags.')
@click.option('-p', '--period', type=(str, str, str), help='Accepts '
              'a start year, (inclusive) end year, and a title')
@click.option('-g', '--group', type=str, help='Accepts a title and'
              'a list of terms to group together.')
def add(manual, period, group):
    '''Add an event or time period. Calling add with no arguments
    will prompt the user for event details to add.
    '''
    # manual = manual event
    if period:
        start_year, end_year, title = period
        start_year = convert_bc_to_neg(start_year).strip()
        end_year = convert_bc_to_neg(end_year).strip()
        title = title.lower()

        confirm_yes_no(f'\n\tStart Year: {start_year}\n'
                       f'\tEnd Year: {end_year}\n'
                       f'\tPeriod Title: {title}\n\n'
                       'Do you want to add this period?',
                       lambda: append_row([start_year, end_year, title],
                                          'periods'),
                       lambda: print('\nPeriod dropped'))
        return
    if group:
        title, *terms = group.split(',')
        title = title.strip().lower()
        terms = [term.strip() for term in terms]
        terms = ','.join(terms)
        confirm_yes_no(f'\n\tTitle: {title}\n'
                       f'\tTerms: {terms}\n\n'
                       'Do you want to add this group?',
                       lambda: append_row([title, terms],
                                          'groups'),
                       lambda: print('\nGroup dropped'))
        return

    if manual:
        year, category, description, *tags = manual.split(',')
        tags = ','.join(tags)
        user_row = {"year": year,
                    "category": category,
                    "description": description,
                    "tags": tags}
    else:
        user_row = get_new_row_from_user()

    user_row = clean_timeline_input(user_row)
    year, _, category, description, tags = user_row

    confirm_yes_no(f'\n\tYear: {year}\n'
                   f'\tCategory: {category}\n'
                   f'\tDescription: {description}\n'
                   f'\tTags: {tags}\n\n'
                   'Do you want to add this event?',
                   lambda: append_row(user_row, 'timeline'),
                   lambda: print('\nEvent dropped'))


@cli.command()
@click.option('-s', '--start-year', type=str,
              help='Get only results starting from start year.')
@click.option('-e', '--end-year', type=str,
              help='Get only results up to end year.')
@click.option('-c', '--category', type=str,
              help='Get only results in a given category.')
@click.option('-g', '--grep', type=str,
              help='Get only results containing given string.')
@click.option('-p', '--period', type=str,
              help='Get only results that fall in a given named time period.')
@click.option('-pl', '--period-list', type=str,
              help='Get the list of currently available time periods.')
def ls(start_year, end_year, category, grep, period, period_list):
    '''
    Prints the timeline with given parameters.
    end_year is INCLUSIVE
    '''
    if period_list:
        for row in format_period_list(list_('periods')):
            click.echo(row)
        return

    timeline_list = list_('timeline')

    if period:
        print(f'Period: {period}\n')
        start_year, end_year = get_period_range(period.strip())

    # Get list from start year
    if not start_year:
        start_year = '10000000000bc'
    start_year = convert_bc_to_neg(start_year).strip()
    timeline_list = [row for row in timeline_list
                     if int(row[0]) >= int(start_year)]

    # Get list from end year
    if end_year:
        end_year = convert_bc_to_neg(end_year).strip()
        timeline_list = [row for row in timeline_list
                         if int(row[0]) <= int(end_year)]

    # Get list with only category
    if category:
        for matcher, cat in CAT_MATCHERS.items():
            if category.lower().strip() == matcher:
                category = cat
                break
        timeline_list = filter_timeline_list('category', category,
                                             timeline_list)

    # Get list with search term
    if grep:
        grep = grep.lower()
        timeline_list = [row for row in timeline_list
                         if grep in (row[3]+row[4]).lower()]

    output = format_timeline_list(sort_timeline_list(timeline_list))
    for row in output:
        click.echo(row)


def lowercasify_periods():
    with open(PATHS['periods'], 'r', newline='') as periodscsv:
        reader = csv.reader(periodscsv, delimiter=',')
        # get a list of periods with the search term partially in title col
        lowercase_periods = []
        periods = [row for row in reader]
        pprint(periods)
        for row in periods:
            new_row = []
            for item in row:
                new_row.append(item.lower())
            lowercase_periods.append(new_row)
        pprint(lowercase_periods)
    with open(PATHS['periods'], 'w', newline='') as periodscsv:
        writer = csv.writer(periodscsv, delimiter=',')
        for row in lowercase_periods:
            writer.writerow(row)


if __name__ == '__main__':
    cli()
