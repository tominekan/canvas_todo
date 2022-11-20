from canvasapi import Canvas
from canvasapi.exceptions import Forbidden
import json
import os
from jsondiff import diff

class SimpleCanvasUser:
    def __init__(self, api_url: str, api_key: str, debug=False):

        """
        Canvas API abtracted to make life easier, so basically based on canvasapi project
        requires api_url, specifies the canvas api https://<yourdisctrict>.instructure.com
        reqiures api_key, this is user specific and user generated
        """


        self.debugOn = debug
        self.canvas = Canvas(api_url, api_key) 
        self.cache_name = os.path.expanduser("~/.cache/canvas_todo/old_assignments.json")
        self.cache_dir = os.path.expanduser("~/.cache/canvas_todo/")
        self.config_name = "canvas_todo.json"
        self.start_time = "5:30"
        # Update list of active courses and active hwk
    
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
        if (not os.path.exists(self.cache_dir)):
            os.mkdir(self.cache_dir)

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
            return newAssignments
        