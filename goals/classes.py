# This module contains custom classes for use in strategicus assessments
#  * These classes need to be manually included in other programs to be referenced
#  * Custom class objects provide a logical structure to store data for
#  * display when leveraging data models becomes too cumbersome


    
########################################################################
#### GOALS
#### This class is used to store the goals
########################################################################
emptyGoal = {'goal_id':-1,'goal':'No Goal Defined','duration':'XX','priority':'-1'}

class task:
    def __init__(self, data):
        self.id = data['goal_id']
        self.name = data['goal']
        self.duration = data['goal_type_id__goal_abbv']
        self.priority = data['priority']

    def __str__(self):
        return self.name
    
class st_goal:
    def __init__(self, data):
        self.id = data['goal_id']
        self.name = data['goal']
        self.duration = data['goal_type_id__goal_abbv']
        self.priority = data['priority']
        self.tasks = []

    def add_task(self, data):
        for item in data:
            self.tasks.append(task(item))

    def __str__(self):
        return self.name
    
class mt_goal:
    def __init__(self, data):
        self.id = data['goal_id']
        self.name = data['goal']
        self.duration = data['goal_type_id__goal_abbv']
        self.priority = data['priority']
        self.st_goals = []

    def add_st_goal(self, data):
        for item in data:
            self.st_goals.append(st_goal(item))

    def __str__(self):
        return self.name
    
class lt_goal:
    def __init__(self, data):
        self.id = data['goal_id']
        self.name = data['goal']
        self.duration = data['goal_type_id__goal_abbv']
        self.priority = data['priority']
        self.mt_goals = []

    def add_mt_goal(self, data):
        for item in data:
            self.mt_goals.append(mt_goal(item))

    def __str__(self):
        return self.name
    
class ll_goal:
    def __init__(self, data):
        self.id = data['goal_id']
        self.name = data['goal']
        self.duration = data['goal_type_id__goal_abbv']
        self.priority = data['priority']
        self.lt_goals = []

    def add_lt_goal(self, data):
        for item in data:
            self.lt_goals.append(lt_goal(item))

    def __str__(self):
        return self.name


class goal:
    def __init__(self, data):
        self.ll_goals = []
        if not data:
            self.ll_goals.append(ll_goal(emptyGoal))
        for item in data:
            self.ll_goals.append(ll_goal(item))
        
    def __str__(self):
        return self.name