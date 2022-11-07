from todoist_api_python.api import TodoistAPI

# Fetch tasks synchronously
def get_tasks_sync():
    api = TodoistAPI("my token")
    try:
        tasks = api.get_tasks()
        print(tasks)
    except Exception as error:
        print(error)

