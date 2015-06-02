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

def get_stagnatingIssues(account_name, assignee_email, token, include_archived, issueAge, assignee_name):

  stagnatingIssues_number = 0

  a = account.Account(account_name, token, include_archived)

  todays_date = date.today()

  html_email_body = ''

  projs = a.projects()

  printed_project_name = False

  something_to_print = False

  for proj in projs:

    printed_project_name = False
    issues = proj.issuesAssignedTo(assignee_email)

    if issues:

      for i in issues:

       if (i.assignee_email == assignee_email) and (i.status != 'Closed') and (get_date(i.updated_at) + timedelta(days=issueAge) < todays_date):
          something_to_print = True
          stagnatingIssues_number += 1
          printable_subject = i.subject.replace(u"\u25ba", "&#9658;").encode('ascii', 'ignore')

          if printed_project_name == False:
            html_email_body += '<li>' + proj.name + '</li>\n<ul>\n'
            printed_project_name = True

          html_email_body += '<li><a href="' + i.url + '" font="Source Sans Pro">' + printable_subject + '</a> - <small>Last update: ' + str(get_date(i.updated_at)) + '</small></li>\n'

    if printed_project_name == True:
      html_email_body += '</ul>\n'

  html_email_body += '</ul></body>\n</html>'

  if something_to_print == True:
    if stagnatingIssues_number == 1:
      html_email_body = '<h3>There is <font size="6">' + str(stagnatingIssues_number) + '</font> issue that has been stagnating for 90+ days assigned to ' + assignee_name + '.</h3>\n<ul>\n' + html_email_bod
    else:
      html_email_body = '<h3>There are <font size="6">' + str(stagnatingIssues_number) + '</font> issues that have been stagnating for 90+ days assigned to ' + assignee_name + '.</h3>\n<ul>\n' + html_email_body
  else:
      html_email_body = '<h3>Good job ' + assignee_name + '! there are <font size="6">0</font> stagnating Sifter issues assigned to you.</h3>\n<ul>\n' + html_email_body
  
  html_email_body = '<html>\n<p>This is an automatic reminder of forgotten Sifter issues. Some are legitimate bugs and others stop being applicable as we make changes. Keeping Sifter clean helps prioritizing issue fixes.</b></p>\n' + html_email_body    

  return html_email_body, str(stagnatingIssues_number)