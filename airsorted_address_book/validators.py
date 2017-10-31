import re

class EmailParamsValidator:
    def check(data):
        if(type(data) is list):
            for element in data:
                if not re.match(r"[^@]+@[^@]+\.[^@]+", element):
                    return False
            return True
        else:
            return False