#!/usr/bin/env python

import argparse
from bs4 import BeautifulSoup
import csv
import json
import logging
import logging.handlers
import os
import pprint
import re
import requests
from urllib.parse import urlparse, quote

def main():

    # Logging.
    debug_log_path = 'prl_joai_admin.debug.log'
    rotating_log_handler = logging.handlers.RotatingFileHandler(debug_log_path, maxBytes=2**20, backupCount=1)
    logging.basicConfig(level=logging.INFO, format='%(levelname)s [%(asctime)s] %(message)s', datefmt='%Y-%m-%d %I:%M:%S %p', handlers=[rotating_log_handler])

    # Command line arguments.
    parser = argparse.ArgumentParser(description='Add (remove) scheduled harvests to (from) jOAI via the command line.')
    parser.add_argument('-J', '--harvester-admin-url',
                        metavar='URL',
                        action='store',
                        default='https://test-joai-harvester.library.ucla.edu/oai/admin/harvester.do',
                        help='jOAI harvester admin URL, ending in \'harvester.do\' (defaults to our test jOAI instance)')
    parser.add_argument('-D', '--delete',
                        action='store_const',
                        const=True,
                        default=False,
                        help='interactively delete scheduled harvests from jOAI before attempting to add any; takes precedence over -i/--csv')
    parser.add_argument('-i', '--csv',
                        metavar='FILE',
                        action='store',
                        default='prl_joai_harvests.csv',
                        help='input CSV file (defaults to the file named \'prl_joai_harvests.csv\' in the working directory)')
    oai_submit_args = vars(parser.parse_args())

    # Get a session cookie from jOAI.
    add_harvest_form_url = '{}{}'.format(oai_submit_args['harvester_admin_url'],
                                         '?button=Add+new+harvest&scheduledHarvest=add'
                                         )
    s = requests.Session()
    harvest_list = s.get(oai_submit_args['harvester_admin_url'])
    print('\nPointed at <{}>.'.format(add_harvest_form_url))

    # First, see if the user wants to delete scheduled harvests.
    if oai_submit_args['delete']:
        print('''
***********************************
**** REMOVE SCHEDULED HARVESTS ****
***********************************''')
        scheduled_harvests = []
        for scheduled_harvest_html in BeautifulSoup(harvest_list.text, 'html.parser').find_all(
                lambda x: x.name == 'tr' and x.has_attr('id') and x['id'] == 'formrow'
                ):

            html_string = scheduled_harvest_html.find('td').text
            parsed_html_string = re.sub(re.compile('\s\s+'), '|', re.sub(re.compile('(<[^a].*?>)|(<a.*>)'), '', html_string)).split('|')

            sh_uid = scheduled_harvest_html.find(lambda x: x.name == 'input' and x.has_attr('name') and x['name'] == 'shUid')['value']
            sh_institution = parsed_html_string[1]
            sh_base_url = parsed_html_string[3]
            sh_harvested_to = parsed_html_string[5]
            sh_set_spec = scheduled_harvest_html.find_all('td', recursive=False)[2].get_text().strip()

            scheduled_harvests.append({
                'shUid': sh_uid,
                'shInstitution': sh_institution,
                'shBaseURL': sh_base_url,
                'shSetSpec': sh_set_spec,
                'shHarvestedTo': sh_harvested_to
                })

        # Enable a custom interactive shell as a convenience for the user.
        interactive_shell_enabled = True

        if scheduled_harvests:
            for scheduled_harvest in scheduled_harvests:
                print('''\nNext scheduled harvest to remove:
    Institution:\t{}
    OAI-PMH base URL:\t{}
    OAI-PMH SetSpec:\t{}
    Harvested to:\t{}\n'''.format(
                            scheduled_harvest['shInstitution'],
                            scheduled_harvest['shBaseURL'],
                            scheduled_harvest['shSetSpec'] or '<none>',
                            scheduled_harvest['shHarvestedTo']
                            ))

                # If interactive shell is disabled, choose [r]emove every time.
                if interactive_shell_enabled:
                    prompt = '[r]emove / [y]es to all / [s]kip / [n]o to all / [h]elp / [q]uit => '
                    action_choice = input(prompt)

                # Handle the help message and user errors.
                while action_choice not in ['r', 'y', 's', 'n', 'q']:
                    if action_choice == 'h':
                        print('Press \'r\' to remove this scheduled harvest from jOAI.')
                        print('Press \'y\' to disable this interactive shell and just remove all scheduled harvests from jOAI.')
                        print('Press \'s\' to skip removing this scheduled harvest from jOAI.')
                        print('Press \'n\' to disable this interactive shell and just skip removing any scheduled harvests from jOAI.')
                        print('Press \'h\' to display this help message.')
                        print('Press \'q\' to stop removing scheduled harvests from jOAI, and exit this program.\n')
                    else:
                        print('Action \'{}\' not recognized.\n'.format(action_choice))
                    action_choice = input(prompt)

                # Handle valid user input.
                # Once the user chooses [y]es to all, the script takes over.
                if action_choice == 'y':
                    print('Kicking off the brakes, here we go...')
                    interactive_shell_enabled = False
                    action_choice = 'r'
                elif action_choice == 'n':
                    print('Skipping all...')
                    interactive_shell_enabled = False
                    action_choice = 's'

                if action_choice == 'r':
                    # Simulate a form submission.
                    request_payload = {
                        'button': 'Delete',
                        'scheduledHarvest': 'delete',
                        'shUid': scheduled_harvest['shUid']
                        }
                    s.post(oai_submit_args['harvester_admin_url'],
                        data=request_payload,
                        cookies=s.cookies
                        )
                    print('\n*** Harvest removed. Check the jOAI admin interface to verify success.')
                elif action_choice == 's':
                    print('Skipped.')
                    continue
                elif action_choice == 'q':
                    print('Bye.')
                    exit()
        else:
            print('\nNo scheduled harvests.')


    # Next, add scheduled harvests from the CSV.
    print('''
**********************************
***** ADD SCHEDULED HARVESTS *****
**********************************''')
    with open(oai_submit_args['csv'], newline='') as csvfile:

        # Enable a custom interactive shell as a convenience for the user.
        interactive_shell_enabled = True

        reader = csv.DictReader(csvfile, quotechar='\'')
        for row in reader:
            if not row['skip']:
                # Print the CSV row in a nice format.
                print('''\nNext scheduled harvest to add:
    Institution:\t{}
    OAI-PMH base URL:\t{}
    OAI-PMH SetSpec:\t{}
    Harvest every {} days at {}\n'''.format(row['Repository name'],
                                        row['Repository base URL'],
                                        row['OAI-PMH SetSpec'] or '<none>',
                                        row['Harvest every X days'],
                                        row['Harvest at time T']
                                        )
                                        )

                # If interactive shell is disabled, choose [a]dd every time.
                if interactive_shell_enabled:
                    prompt = '[a]dd / [y]es to all / [s]kip / [n]o to all / [h]elp / [q]uit => '
                    action_choice = input(prompt)

                # Handle the help message and user errors.
                while action_choice not in ['a', 'y', 's', 'n', 'q']:
                    if action_choice == 'h':
                        print('Press \'a\' to add this scheduled harvest to jOAI.')
                        print('Press \'y\' to disable this interactive shell and just add all scheduled harvests to jOAI.')
                        print('Press \'s\' to skip adding this scheduled harvest to jOAI.')
                        print('Press \'n\' to disable this interactive shell and just skip adding any scheduled harvests to jOAI.')
                        print('Press \'h\' to display this help message.')
                        print('Press \'q\' to stop adding scheduled harvests to jOAI, and exit this program.\n')
                    else:
                        print('Action \'{}\' not recognized.\n'.format(action_choice))
                    action_choice = input(prompt)

                # Handle valid user input.
                # Once the user chooses [y]es to all, the script takes over.
                if action_choice == 'y':
                    print('Kicking off the brakes, here we go...')
                    interactive_shell_enabled = False
                    action_choice = 'a'
                elif action_choice == 'n':
                    print('Skipping all...')
                    interactive_shell_enabled = False
                    action_choice = 's'

                if action_choice == 'a':
                    # Simulate a form submission.
                    collection_dir = row['OAI-PMH SetSpec'] or row['Set directory']
                    request_payload = {
                        'shUid': '0',
                        'scheduledHarvest': 'save',
                        'shRepositoryName': row['Repository name'],
                        'shBaseURL': row['Repository base URL'],
                        'shSetSpec': row['OAI-PMH SetSpec'],
                        'shMetadataPrefix': 'oai_dc',
                        'shEnabledDisabled': 'enabled',
                        'shHarvestingInterval': row['Harvest every X days'],
                        'shIntervalGranularity': 'days',
                        'shRunAtTime':  row['Harvest at time T'],
                        'shDir': 'custom',
                        'shHarvestDir': '/joai/data/{}/{}'.format(urlparse(row['Repository base URL']).netloc, collection_dir),
                        's': '+',
                        'shDontZipFiles': 'true',
                        'shSet': 'split' if collection_dir == '' else 'dontsplit'
                    }
                    r = s.post(oai_submit_args['harvester_admin_url'],
                            data=request_payload,
                            cookies=s.cookies
                            )

                    # If there was an error, there will be red font tags in the HTML response.
                    red_font_tags = BeautifulSoup(r.text, 'html.parser').find_all(
                        # finds <font color="red">...</font>
                        lambda x: x.name == 'font' and x.has_attr('color') and x['color'] == 'red'
                        )

                    if len(red_font_tags) > 0:
                        logging.error(
                            '\n'.join([
                                'Harvest was not saved.',
                                json.dumps(row, indent=4),
                                '\n'.join([tag.string for tag in red_font_tags])
                                ]) + '\n'
                            )
                        print('\n!!! Harvest was not saved. See {} for details.'.format(os.path.abspath(debug_log_path)))
                    else:
                        print('\n*** Harvest saved. Check the jOAI admin interface to verify success.')
                elif action_choice == 's':
                    print('Skipped.')
                    continue
                elif action_choice == 'q':
                    print('Bye.')
                    exit()
        print('\nNo more rows.')
        print('Bye.')

if __name__ == '__main__':
    main()
