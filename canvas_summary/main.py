from simplecanvasuser import SimpleCanvasUser
from pprint import pprint
from os import environ
CANVAS_API_URL = "https://smuhsd.instructure.com/"
CANVAS_API_KEY = environ.get("CANVAS_KEY")

user = SimpleCanvasUser(CANVAS_API_URL, CANVAS_API_KEY)
pprint(user.active_courses)
pprint(user.current_hwk)
