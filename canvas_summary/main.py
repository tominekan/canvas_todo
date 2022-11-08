from simplecanvasuser import SimpleCanvasUser
from pprint import pprint
API_URL = "https://smuhsd.instructure.com/"
API_KEY = "tonka"

user = SimpleCanvasUser(API_URL, API_KEY)
pprint(user.active_courses)
pprint(user.current_hwk)
