#!/bin/python
# coding: utf-8

import sys
import requests
from bs4 import BeautifulSoup
import re
from optparse import OptionParser
import json

VERBOSE_MODE = False

def display_message(s):
    global VERBOSE_MODE
    if VERBOSE_MODE:
        print '[verbose] %s' % s

def request_results(company_name):
    return requests.get('http://www.email-format.com/i/search_result/?q=%s' % (company_name)).content

def company_exists(content):
    return 'No results found for' not in content

def multiple_companies(content):
    return 'Search for Domains' in content

def iterate_on_all_companies(content):
    soup = BeautifulSoup(content)
    companies = {}
    for company in soup.findAll('a', attrs={'class': 'block'}):
        # sanitize retrieved results
        companyName = sanitize_string(company.text)
        companyUrl = sanitize_string(company['href'])

        # print companyName + ' ' + companyUrl
        companies[companyName] = companyUrl
    return companies

def sanitize_string(string):
    return string.replace('\n', '').replace('\t', '').replace(' ', '')

def get_mails(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.content)
    res = []
    for mail in soup.findAll('div', attrs={'class': 'fl'}):
        mailAdress = sanitize_string(mail.text)
        if '@' in mailAdress and not 'e.g.' in mailAdress:
            res.append(mailAdress)
    return res

def main():
    global VERBOSE_MODE
    parser = OptionParser()
    parser.add_option("-c", "--company", dest="company", help="Company you want to retrieve mails", default=None)
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="Verbose mode")

    (options, args) = parser.parse_args()

    if options.verbose:
        VERBOSE_MODE = True

    if options.company is not None:
        print 'Fetching result for company "%s"' % (options.company)
    else:
        print parser.print_help()
        sys.exit(-1)

    # no results
    req = request_results(options.company)
    if (not company_exists(req)):
        print 'Company %s does not exist.' % (options.company)

    # several companies
    if (multiple_companies(req)):
        companies = iterate_on_all_companies(req)
        for company in companies:
            print '%s' % (company)
        index = raw_input('Select company: ')
        mails = get_mails('http://www.email-format.com%s' % companies[index])
        print mails
        # print companies[index]
        # print companies
    else:
        # one company
        mails = get_mails('http://www.email-format.com/i/search_result/?q=%s' % (options.company))
        print mails

if __name__ == '__main__':
    main()
