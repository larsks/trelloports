#!/usr/bin/python

import os
import sys
import argparse
import yaml
import pprint
import time
import logging

import jinja2
from trollop import TrelloConnection

def find_organization(me, name):
    for org in me.organizations:
        if org.name == name:
            return org

    raise KeyError(name)

def find_board(org, name):
    for board in org.boards:
        if board.name == name:
            return board

    raise KeyError(name)

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('-f', '--config', default='trello.yml')
    p.add_argument('-o', '--output')
    p.add_argument('-v', '--verbose', action='store_true')
    p.add_argument('-T', '--templates', default='templates')
    return p.parse_args()

def main():
    opts = parse_args()
    with open(opts.config) as fd:
        cf = yaml.load(fd)

    logging.basicConfig(
            level = logging.INFO if opts.verbose else logging.WARN)

    tc = TrelloConnection(cf['trello']['apikey'], cf['trello']['token'])
    
    org = find_organization(tc.me, cf['report']['organization'])
    logging.info('using organization: %s (%s)',
            org.displayname, org.name)
    board = find_board(org, cf['report']['board'])
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

    logging.info('generating report')
    with open(opts.output, 'w') if opts.output else sys.stdout as fd:
        env = jinja2.Environment(
                loader=jinja2.loaders.FileSystemLoader(opts.templates))
        template = env.get_template('report.md')
        print >>fd, template.render(report=report,
                date=time.strftime('%Y-%m-%d', time.localtime()))

if __name__ == '__main__':
    main()


