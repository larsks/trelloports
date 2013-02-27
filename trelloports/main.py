#!/usr/bin/python

import os
import sys
import argparse
import yaml
import pprint
import time
import logging

import jinja2
import trollop

opts = None
config = None

try:
    test_connection = trollop.TrelloConnection('dummy', 'dummy')
except TypeError:
    import requests

    # This works around a bug in trollop with requests 1.1.0.
    class TrelloConnection (trollop.TrelloConnection):
        def __init__(self, api_key, oauth_token):
            self.session = requests.session()
            self.key = api_key
            self.token = oauth_token

    trollop.TrelloConnection = TrelloConnection

def find_organization(me, name):
    for org in me.organizations:
        if org.name == name:
            return org

    raise KeyError(name)

def find_board(src, name):
    for board in src.boards:
        if board.name == name:
            return board

    raise KeyError(name)

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('-f', '--config', default='trello.yml')
    p.add_argument('-o', '--output')
    p.add_argument('-v', '--verbose', action='store_true')
    p.add_argument('-T', '--templates')
    return p.parse_args()

def gather_info(tc):
    global opts
    global config

    if 'organization' in config['report']:
        org = find_organization(tc.me, config['report']['organization'])
        logging.info('using organization: %s (%s)',
                org.displayname, org.name)
        board = find_board(org, config['report']['board'])
    else:
        board = find_board(tc.me, config['report']['board'])

    logging.info('using board: %s', board.name)
    report = {}
    for list in board.lists:
        logging.info('processing list: %s', list.name)
        report[list.name] = []
        for card in list.cards:
            this_card = {
                'title': card.name,
                'description': card.desc,
                'checklists': []}
            for checklist in card.checklists:
                this_checklist = {
                        'title': checklist.name,
                        'items': [],
                        }
                for item in checklist.checkItems:
                    this_checklist['items'].append(item.name)
                this_card['checklists'].append(this_checklist)

            report[list.name].append(this_card)

    return report

def generate_report(report):
    global opts
    global config

    logging.info('generating report')
    with open(opts.output, 'w') if opts.output else sys.stdout as fd:
        if opts.templates:
            loader = jinja2.loaders.FileSystemLoader(opts.templates)
        else:
            loader = jinja2.loaders.PackageLoader('trelloports')

        env = jinja2.Environment(loader=loader)
        template = env.get_template('report')
        print >>fd, template.render(report=report,
                date=time.strftime('%Y-%m-%d',
                    time.localtime())).encode('utf-8')


def main():
    global opts
    global config

    opts = parse_args()
    with open(opts.config) as fd:
        config = yaml.load(fd)

    logging.basicConfig(
            level = logging.INFO if opts.verbose else logging.WARN)

    tc = TrelloConnection(config['trello']['apikey'], config['trello']['token'])
    report = gather_info(tc)
    generate_report(report)
    
if __name__ == '__main__':
    main()

