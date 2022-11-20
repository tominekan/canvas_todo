from todoist_api_python.api import TodoistAPI
from os import environ

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


