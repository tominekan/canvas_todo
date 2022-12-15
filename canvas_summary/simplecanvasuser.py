from canvasapi import Canvas
from canvasapi.exceptions import Forbidden
import json
import os
from jsondiff import diff
import time
from os import environ
from todoist_api_python.api import TodoistAPI

class TodoistProject:
    def __init__(self, api_key: str, project_name: str, debug=False):

        """
        TodoistProject, this simulates a single todoist project,
        which is all I need for this project, you can only add or get tasks
        which again, is all I need.
        """


        self.api = TodoistAPI(api_key)
        self.debugOn = debug
        self.project_id = self.__selectProjects(project_name)
        if (self.project_id == -1):
            raise Exception("Data can't be extracted")
        
    
    def __debugPrint(self, *args):
        if (self.debugOn):
            print(args)

    def __selectProjects(self, project_name):
        try:

            for project in self.api.get_projects():
                if (project.name == project_name):
                    self.__debugPrint(f"{project.name} MATCH!")
                    return project.id
                self.__debugPrint(f"{project.name} not a match")
        except Exception as e:
            self.__debugPrint("Error: ")
            self.__debugPrint(e)
            return -1

    
    def getProjectTasks(self):
        """
        Gets all the tasks in a specific project
        returns -1 if not successful
        """

        try:
            self.__debugPrint(f"Getting Tasks for project: {self.project_id}")
            return self.api.get_tasks(project_id=self.project_id)
        except Exception as e:
            self.__debugPrint("Error: ")
            self.__debugPrint(e)
            return -1
    
    def addTask(self, content, due_date):

        """
        Add a single task to a specific project, takes the name of the task and the due date
        returns -1 if not successful
        """


        try:
            self.__debugPrint(f"Adding task \"{content}\": due {due_date} to project: {self.project_id}")
            self.api.add_task(content=content, due_string=due_date, due_lang="en", project_id=self.project_id)
        except Exception as e:
            self.__debugPrint("Error: ")
            self.__debugPrint(e)
            return -1

class SimpleCanvasUser:
    def __init__(self, api_url: str, api_key: str, debug=False):

        """
        Canvas API abtracted to make life easier, so basically based on canvasapi project
        requires api_url, specifies the canvas api https://<yourdisctrict>.instructure.com
        reqiures api_key, this is user specific and user generated
        """


        self.debugOn = debug
        self.canvas = Canvas(api_url, api_key) 
        path, filename = os.path.split(os.path.realpath(__file__))
        self.cache_name = path + "\\" + os.path.expanduser("old_assignments.json")
    
    def getActiveCourses(self) -> list:

        """
        Gets list of classes that the user is currently enrolled in
        returns a list of Strings
        """


        course_names = []
        for course in self.canvas.get_courses(enrollment_status="active"):
            try:
                if (self.debugOn):
                    print(course)
                course_names.append(str(course))
            except AttributeError: # 
                if (self.debugOn):
                    print("AttributeError: This seems to be normal tho")
                break
            except Exception as e:
                if (self.debugOn):
                    print("Error Here vvvvv")
                    print(e)
                break
        return course_names

    def __getActiveCourses(self) -> list:

        """
        (INTERNAL FUNCTION)
        Gets list of classes that the user is currently enrolled in
        returns a list of Course objects
        """

        course_list = []
        for course in self.canvas.get_courses(enrollment_status="active"):
            try:
                if (self.debugOn):
                    print(course)
                course_list.append(course)
            except AttributeError: # 
                if (self.debugOn):
                    print("AttributeError: This seems to be normal tho")
                break
            except Exception as e:
                if (self.debugOn):
                    print("Error Here vvvvv")
                    print(e)
                break
        return course_list

    def __debugPrint(self, *args):
        if (self.debugOn):
            print(args)
    

    def getAssignments(self) -> dict:

        """
        Gets all assignments upcoming and overdue
        also updates self.current_hwk
        Returns dict of lists containing Assignment objects, something like
        {
            "upcoming": [Assignment, Assignment],
            "overdue": [Assignment, Assignment],
        }
        """


        courses_name = {"upcoming": [], "overdue": []}
        
        try:
            for course in self.__getActiveCourses():
                for assignment in course.get_assignments(bucket="upcoming"):
                    self.__debugPrint(f"Upcoming: {assignment}")
                    courses_name["upcoming"].append(str(assignment))
            
                for assignment in course.get_assignments(bucket="overdue"):
                    self.__debugPrint(f"Overdue: {assignment}")
                    courses_name["overdue"].append(str(assignment))
        except Forbidden:
            self.__debugPrint("canvasapi.exceptions.Forbidden: This also seems to be normal")
        except Exception as e:
            self.__debugPrint("Error Here vvvvv")
            self.__debugPrint(e)
            
        
        return courses_name
    
    def getNewAssignments(self):
        
        """
        Get all new assignments
        """


        activeHwk = self.getAssignments()

        if os.path.exists(self.cache_name): # not first time run
            fp = open(self.cache_name, 'r')
            old_data = json.load(fp) # Load up the old data
            fp.close()
            
            diffs = diff(old_data, activeHwk) # get difference between old and new hwk

            with open(self.cache_name, "w") as cache:
                json.dump(activeHwk, cache) # dump new data
            
            if (len(diffs) == 0):
                return None
            else:
                if "upcoming" in diffs:
                    print("new assignments")
                    assignmentDiffs = list(diffs["upcoming"].values())[0]
                    print(assignmentDiffs)
                    newAssignemnts = []
                    for assignment in assignmentDiffs:
                        newAssignemnts.append(assignment[1])
                    return newAssignemnts
                    
        else: # If script hasn't been run before, then all active courses are new courses
            newAssignments = []
            for assignment in activeHwk["upcoming"]:
                newAssignments.append(assignment)
            for assignment in activeHwk["overdue"]:
                newAssignments.append(assignment)
                
            with open(self.cache_name, "w") as cache:
                json.dump(activeHwk, cache) # dump new data
            return newAssignments


def addTasks(canvas_user, todoist_api):
    
    new_assignments = canvas_user.getNewAssignments()

    if type(new_assignments) == list:
        for assignment in new_assignments:
           todoist_api.addTask(content=assignment, due_date="tomorrow")
    else:
        print("Nothing New :)")



def runFunc():
    # Load up keys
    keys = {"todoist": "", "canvas": ""}
    with open("config.json") as keyfiles:
        data = json.load(keyfiles)
        keys["todoist"] = data["todoist_key"]
        keys["canvas"] = data["canvas_key"]

    CANVAS_API_URL = "https://smuhsd.instructure.com/"
    CANVAS_API_KEY = keys["todoist"]

    user = SimpleCanvasUser(CANVAS_API_URL, keys["canvas"])

    todoist_api = TodoistProject(
        api_key=environ.get("TODOIST_KEY"),
        project_name="The Drill"
    )

    while True:
        addTasks(user, todoist_api)
        time.sleep(3600)

runFunc()