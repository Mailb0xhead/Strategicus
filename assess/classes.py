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
        self.answer = -1

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

    def __str__(self):
        return self.name  