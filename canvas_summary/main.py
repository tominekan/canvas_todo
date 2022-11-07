from simplecanvasuser import SimpleCanvasUser
from pprint import pprint
API_URL = "https://smuhsd.instructure.com/"
API_KEY = "3533~cFOiR8PTZ1fkhvmHpUzf3a4Q4ukv98Mmwe1J8cFnHboPyuHxwqtuzZDmlxh0cVdj"

user = SimpleCanvasUser(API_URL, API_KEY)
pprint(user.active_courses)
pprint(user.current_hwk)