

class ProfileABC(object):

    def do_initial_login_page(self):
        """
        Returns a dict of:
            res: True for StatusCode=200 on connection to login page, False if non-200 status code. If false, rest of dict fields will be unpopulated.
            url: url of form action.
            fields: data fields extracted from input form.
        """
        return None

    def do_logon_request(self, url, field_dict):
        return None