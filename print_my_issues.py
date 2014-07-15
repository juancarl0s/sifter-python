#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       my_issues_page.py
#       
#       Copyright 2012 Mark Mikofski <marko@bwanamaro@yahoo.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#       
#       

import account
import time
from time import mktime
from datetime import datetime, timedelta, date

def get_date(d):
   return datetime.fromtimestamp(mktime(time.strptime(d, '%Y-%m-%dT%H:%M:%SZ'))).date()

account_name = 'enter your sifter account name here, e.g., niche'
token = 'enter your API token here'
opener_name = 'enter your first and last name'
start_date = date(2013, 8, 1) # replace with your desired start date

a = account.Account(company_name, token)

f = open('index.html', 'w')
f.write('<html><body><ol>')

projs = a.projects()

for proj in projs:
   issues = proj.issues()
   for i in issues:
     if i.opener_name.lower() != opener_name: continue
     if get_date(i.created_at) < start_date: continue
     if i.priority.lower() == 'trivial': continue
     if i.category_name:
        if i.category_name.lower() == 'not an issue': continue
        if i.category_name.lower() == 'unsure if it\'s an issue': continue
    
     printable_subject = i.subject.encode('ascii', 'replace')
     f.write('<li><a href="%s">%s</a> - %s, %s, %s, %s</li>' % (i.url, printable_subject, proj.name, i.priority, i.category_name, i.created_at))

f.write('</ol></body></html>')
f.close()
