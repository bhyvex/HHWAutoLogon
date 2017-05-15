
class App:

    __conf = {"wireless_access_point_names":    ['linksys806B', 'linksys 711B', 'linksys'],
        "login_page":                           "http://192.168.100.1:3990/prelogin",
        "login_form_root":                      "http://192.168.100.1/uam/",
        "username":                             "",
        "password":                             "",
        "is_at_hotspot_location_max_tries":     3,
        "is_at_hotspot_location_max_value":     5,
        "ping_disconnected_max_tries":          3,
        "ping_disconnected_max_value":          5,
        "ping_connected_max_tries":             3,
        "ping_connected_max_value":             5
    }
    __setters = ["username", "password"]

    @staticmethod
    def config(name):
        return App.__conf[name]

    @staticmethod
    def set(name, value):
        if name in App.__setters:
            App.__conf[name] = value
        else:
            raise NameError("Name not accepted in set() method")