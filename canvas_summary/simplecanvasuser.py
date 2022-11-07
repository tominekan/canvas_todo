from canvasapi import Canvas
from canvasapi.exceptions import Forbidden

class SimpleCanvasUser:
    def __init__(self, api_url: str, api_key: str, debug=False):

        """
        Canvas API abtracted to make life easier, so basically based on canvasapi project
        requires api_url, specifies the canvas api https://<yourdisctrict>.instructure.com
        reqiures api_key, this is user specific and user generated
        """


        self.debugOn = debug
        self.canvas = Canvas(api_url, api_key) 
        self.active_courses = []
        self.current_hwk = {}
        # Update list of active courses and active hwk
        self.getActiveCourses()
        self.getAssignments()
    
    def getActiveCourses(self) -> list:

        """
        Gets list of classes that the user is currently enrolled in
        also updates self.active_courses
        returns a list of Course objects
        """


        course_list = []
        course_names = []
        for course in self.canvas.get_courses(enrollment_status="active"):
            try:
                if (self.debugOn):
                    print(course)
                course_list.append(course)
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
        self.active_courses = course_names
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


        courses_list = {"upcoming": [], "overdue": []}
        courses_name = {"upcoming": [], "overdue": []}
        
        try:
            for course in self.getActiveCourses():
                for assignment in course.get_assignments(bucket="upcoming"):
                    self.__debugPrint(f"Upcoming: {assignment}")
                    courses_list["upcoming"].append(assignment)
                    courses_name["upcoming"].append(str(assignment))
            
                for assignment in course.get_assignments(bucket="overdue"):
                    self.__debugPrint(f"Overdue: {assignment}")
                    courses_list["overdue"].append(assignment)
                    courses_name["overdue"].append(str(assignment))
        except Forbidden:
            self.__debugPrint("canvasapi.exceptions.Forbidden: This also seems to be normal")
        except Exception as e:
            self.__debugPrint("Error Here vvvvv")
            self.__debugPrint(e)
            
        
        self.current_hwk = courses_name
        return courses_list