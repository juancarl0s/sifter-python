class Issue(object):
    """Representation of an Issue in Sifter"""
    def __init__(self, issue, account):
        self._account = account
        self.number = issue['number']
        self.subject = issue['subject']
        self.description = issue['description']
        self.priority = issue['priority']
        self.status = issue['status']
        self.assignee_name = issue['assignee_name']
        self.assignee_email = issue['assignee_email']        
        self.category_name = issue['category_name']
        self.milestone_name = issue['milestone_name']
        self.opener_name = issue['opener_name']
        self.url = issue['url']
        self.api_url = issue['api_url']
        self.comment_count = issue['comment_count']
        self.created_at = issue['created_at']
        self.updated_at = issue['updated_at']
