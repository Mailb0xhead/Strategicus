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
        self.quest_ids = []
        self.actions = []

    def add_questions(self, data):
        for q in data:
            self.questions.append(questions(q))
            self.quest_ids.append(q['question_id'])

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