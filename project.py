import issue


class Project(object):
    """Representation of a project in Sifter"""
    def __init__(self, project, account):
        self._account = account
        self.issues_url = project['issues_url']
        self.archived = project['archived']
        self.url = project['url']
        self.api_url = project['api_url']
        self.milestones_url = project['milestones_url']
        self.api_people_url = project['api_people_url']
        self.api_issues_url = project['api_issues_url']
        self.api_milestones_url = project['api_milestones_url']
        self.api_categories_url = project['api_categories_url']
        self.name = project['name']
        self.primary_company_name = project['primary_company_name']

    def issuesAssignedTo(self, user_email):
            """Gets all the issues for a given project"""
            issues = []

            # Set per_page to 25 issues per page
            first_page = self.api_issues_url + '?per_page=25&page=1'

            # Get page one
            json_raw = self._account.request(first_page)

            # Set the next page
            next_page = json_raw['next_page_url']

            # Set the number of pages
            number_of_pages = json_raw['total_pages']

            for current_page in range(number_of_pages):
                # Create a wrapper for each issue, add it to the list
                raw_issues = json_raw['issues']
                for raw_issue in raw_issues:
                    i = issue.Issue(raw_issue, self._account)
                    if (i.assignee_email == user_email) and (i.status != 'Closed'):
                        issues.append(i)

                # Make a request for the next page
                if current_page < number_of_pages - 1:
                    # store the results
                    json_raw = self._account.request(next_page)

                # set the next page
                next_page = json_raw['next_page_url']

            return issues

