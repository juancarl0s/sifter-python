#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       stagnatingIssues.py
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

def get_stagnatingIssues(account_name, assignee_email, token, include_archived, issueAge):

  a = account.Account(account_name, token, include_archived)

  todays_date = date.today()

  html_email_body = '<html>\n<body>\n<ul>\n'

  projs = a.projects()

  printed_project_name = False

  something_to_print = False

  for proj in projs:

    html_email_body += '<ul>'
    printed_project_name = False
    issues = proj.issuesAssignedTo(assignee_email)

    if issues:

      for i in issues:

       if (i.assignee_email == assignee_email) and (i.status != 'Closed') and (get_date(i.updated_at) + timedelta(days=issueAge) < todays_date):
          something_to_print = True
          printable_subject = i.subject.replace(u"\u25ba", "&#9658;").encode('ascii', 'ignore')

          if printed_project_name == False:
            html_email_body += '<li><a href="' + proj.issues_url + '">' + proj.name + '</a></li>\n<ul>\n'
            printed_project_name = True

          html_email_body += '<li><a href="' + i.url + '">' + printable_subject + '</a> - <small>Last update: ' + str(get_date(i.updated_at)) + '</small></li>\n'

      html_email_body += '</ul>\n'

    html_email_body += '</ul>\n'

  html_email_body += '</body>\n</html>'

  if something_to_print == True:
    return html_email_body
  else:
    return '0' 