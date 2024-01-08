# This module contains custom classes for use in strategicus assessments
#  * These classes need to be manually included in other programs to be referenced
#  * Custom class objects provide a logical structure to store data for
#  * display when leveraging data models becomes too cumbersome


########################################################################
### QUESTIONS
###     This class contains the data for a question on an assessment
########################################################################

class questions:
    def __init__(self, data):
        self.id = data['question_id']
        self.question = data['question']
        self.answer = 9
        self.level = data['level']
        self.type = data['type']
        self.section = data['section_id__name']

    def __str__(self):
        return self.name
    
########################################################################
### ACTIONS
###     This class contains the data for an action on an assessment
########################################################################
class actions:
    def __init__(self, data):
        self.id = data['question_id__outcome_id']
        self.name = data['actions']
        self.priority = data['priority']
        self.benefit = data['benefit']

    def __str__(self):
        return self.name

########################################################################
### SECTIONS
###     This class contains the data for section of a question on an assessment
########################################################################
class sections:
    def __init__(self, data, sid):
        self.name = data
        self.id = sid
        self.questions = []

    def __str__(self):
        return self.name

########################################################################
### ASSESS
###     This class contains the data for the assessment being reviewed
########################################################################
class assess:
    def __init__(self, data):
        self.id = 0
        self.name = data
        self.questions = []
        self.sections = []
        self.quest_ids = []
        self.actions = []

    def add_questions(self, data):
        self.subcomp = data[0]['subcomp__name']
        curr_section_name = data[0]['section_id__name']
        curr_section = sections(curr_section_name, data[0]['section_id'])

        for q in data:
            print(q['section_id__name'], curr_section_name)
            if q['section_id__name'] != curr_section_name:
                print("adding section")
                self.sections.append(curr_section)
                curr_section_name = q['section_id__name']
                curr_section = sections(curr_section_name, q['section_id'])
            # print(curr_section.name, curr_section.questions)
            curr_section.questions.append(questions(q))
            self.questions.append(questions(q))
            self.quest_ids.append(q['question_id'])
        self.sections.append(curr_section)

        

    def add_scores(self,data):
        for q in self.questions:
            for s in data:
                if s['question_id'] == q.id:
                    q.answer = s['score']
                    break

    def add_actions(self,data):
        for action in data:
            self.actions.append(actions(action))


    def __str__(self):
        return self.name  

#######################################################################
### Engagements
###     This class contains the data for the rengagements being recommended
########################################################################
class engage:
    def __init__(self, data):
        print(data)
        self.id = 0
        self.name = data['eng_name']
        self.sol_type = data['resource_id__resource_type']
        self.desc = data['eng_desc']
        self.type = data['eng_type']
        self.cost = data['eng_cost']
        self.level = data['eng_level']
        self.complexity = data['eng_complexity']
        self.duration = data['eng_duration']
        self.duration_units = data['eng_duration_units']
        self.link = data['eng_link']
        self.rating = data['eng_rating']

    def __str__(self):
        return self.name
    
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