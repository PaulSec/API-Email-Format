"""
This is the (unofficial) Python API for email-format.com Website.

Using this code, you can retrieve emails from the specified company

"""
#!/bin/python
# coding: utf-8

import requests
from bs4 import BeautifulSoup

URL = "http://www.email-format.com"

#def display_message(s):
#    global VERBOSE_MODE
#    if VERBOSE_MODE:
#        print '[verbose] %s' % s


class EmailFormatAPI(object):

    """
        EmailFormatAPI Main Handler
    """

    _instance = None
    _verbose = False

    def __init__(self, arg=None):
        pass

    def __new__(cls, *args, **kwargs):
        """
            __new__ builtin
        """
        if not cls._instance:
            cls._instance = super(EmailFormatAPI, cls).__new__(
                cls, *args, **kwargs)
            if (args and args[0] and args[0]['verbose']):
                cls._verbose = True
        return cls._instance

    def display_message(self, s):
        if (self._verbose):
            print '[verbose] %s' % s

    def search_company(self, company_name):
        return requests.get('%s/i/search_result/?q=%s' % (URL, company_name))

    def company_exists(self, content):
        return 'No results found for' not in content

    def multiple_companies(self, content):
        return 'Search for Domains' in content

    def iterate_on_all_companies(self, content):
        soup = BeautifulSoup(content)
        companies = {}
        for company in soup.findAll('a', attrs={'class': 'block'}):
            # sanitize retrieved results
            companyName = self.sanitize_string(company.text)
            companyUrl = self.sanitize_string(company['href'])

            self.display_message(companyName + ' ' + companyUrl)
            companies[companyName] = companyUrl
        return companies

    def sanitize_string(self, string):
        return string.replace('\n', '').replace('\t', '').replace(' ', '')

    def get_mails(self, content):
        soup = BeautifulSoup(content)
        res = []
        for mail in soup.findAll('div', attrs={'class': 'fl'}):
            mailAdress = self.sanitize_string(mail.text)
            if '@' in mailAdress and not 'e.g.' in mailAdress:
                res.append(mailAdress)
        return res

    def get(self, company):
        self.display_message('Fetching result for company "%s"' % (company))

        req = requests.get('%s/d/%s/' % (URL, company))
        # company cannot be accessed directly
        if '/i/main/' in req.url:
            req = self.search_company(company)
            # if does not exist
            if (not self.company_exists(req.content)):
                self.display_message('Company %s does not exist.' % (company))
                return []

            # if single choice
            if 'email-format.com/d/' in req.url:
                mails = self.get_mails(req.content)

            # if multiple choice
            if (self.multiple_companies(req.content)):
                companies = self.iterate_on_all_companies(req.content)
                for company in companies:
                    print '%s' % (company)
                index = raw_input('Select company: ')
                req = requests.get('%s%s' % (URL, companies[index]))
                mails = self.get_mails(req.content)
        else:
            # can be accessed directly
            mails = self.get_mails(req.content)
        return mails
