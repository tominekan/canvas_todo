from simplecanvasuser import SimpleCanvasUser
from todoist import TodoistProject
import schedule
import time

from os import environ
CANVAS_API_URL = "https://smuhsd.instructure.com/"
CANVAS_API_KEY = environ.get("CANVAS_KEY")

user = SimpleCanvasUser(CANVAS_API_URL, CANVAS_API_KEY)

todoist_api = TodoistProject(
    api_key=environ.get("TODOIST_KEY"),
    project_name="The Drill"
)

def addTasks():
    
    new_assignments = user.getNewAssignments()

    if type(new_assignments) == list:
        for assignment in new_assignments:
           todoist_api.addTask(content=assignment, due_date="tomorrow")
    else:
        print("Nothing New :)")

schedule.every().hour.do(addTasks)

while True:
    schedule.run_pending()
    time.sleep(1)