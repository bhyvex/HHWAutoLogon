
class App(object):
    __wireless_access_point_names = ['linksys806B', 'linksys 711B', 'linksys']
    __login_page = "http://192.168.100.1:3990/prelogin"
    __login_form_root = "http://192.168.100.1/uam/"
    __username = ""
    __password = ""
    __is_at_hotspot_location_max_tries = 3
    __is_at_hotspot_location_max_value = 5
    __ping_disconnected_max_tries = 3
    __ping_disconnected_max_value = 5
    __ping_connected_max_tries = 3
    __ping_connected_max_value = 5

    @staticmethod
    def config(name):
        return App.__dict__["_App__"+name]

    @staticmethod
    def set(name, value):
        setters = ["username", "password"]
        if name in setters:
            #App.__dict__["_App__" + name] = value
            vars()["_App__" + name] = value
        else:
            raise NameError("Name not accepted in set() method")


