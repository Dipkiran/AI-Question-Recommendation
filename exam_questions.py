import os
import json
import re
from bs4 import BeautifulSoup

class ExamQuestions:
    def __init__(self, instance_source, question_source, train_semester, test_semester):
        self.question_source = question_source
        self.instance_source = instance_source
        self.train_semester = train_semester
        self.test_semester = test_semester
        self.all_exam_instances = {}
        self.train_questions = {}
        self.test_questions = {}
    
    def exam_instances_per_semester(self):
        exam_instances_semester = os.listdir(self.instance_source)
        return [{exam_folder: "%s/%s"%(self.instance_source,exam_folder)} for exam_folder in exam_instances_semester]
    
    def get_all_exam_instances_per_semester(self, folder):
        folder_link = "%s/assessments"%(folder)
        if os.path.exists(folder_link):
            exam_folder_link = os.listdir(folder_link)
            exam_instances = [f for f in exam_folder_link if "exam" in f and ("practice" not in f and "makeup" not in f)]
            instances_per_semester_link = ["%s/%s/%s"%(folder_link, f, "infoAssessment.json") for f in exam_folder_link if f in exam_instances]
            return instances_per_semester_link
    
    def get_exam_instances_per_semester(self, exam_instances, semester):
        exam_instance_id = {}
        for exam_instance in exam_instances:
            exam = str(exam_instance.split('assessments')[1]).split("/")[1]
            exam_instances = []
            with open(exam_instance, "r") as file:
                data = json.load(file)
                exam_instances_zones_list = data['zones']
                for instances_zones in exam_instances_zones_list:
                    for ins_link in (instances_zones['questions']):
                        if ins_link.get('id'):
                            exam_instances.append(ins_link['id'])
                        else:
                            for ins in ins_link['alternatives']:
                                exam_instances.append(ins['id'])
            exam_instance_id[exam] = exam_instances
        self.all_exam_instances[semester] = exam_instance_id
    
    def get_all_questions(self):
        for semester, exams in self.all_exam_instances.items():
            self.exam_questions = {}
            for exam, exam_questions in exams.items():
                question_list = []
                for exam_question in exam_questions:
                    question_folder = self.question_source + "/" + exam_question
                    if(os.path.exists(question_folder)):
                        question_link = question_folder + "/question.html"
                        with open(question_link, 'r', encoding='utf-8') as file:
                            html_content = file.read()
                            soup = BeautifulSoup(html_content, 'html.parser')
                            question = ""
                            for ques in soup.find_all('pl-question-panel'):
                                question += ques.get_text()
                            if "{{" in question and "server.py" in os.listdir(question_folder):
                                python_file_link = question_folder + "/server.py"
                                with open(python_file_link, 'r', encoding='utf-8') as file:
                                    python_content = file.read()
                                    question = question + " " + python_content
                            question = question.replace("\n", " ")
                            question = question.replace("\"", "'")
                            question = re.sub(r"\s+", " ", question).strip()
                            question_list.append(question)
                self.exam_questions[exam] = question_list
            if semester in self.train_semester:
                self.train_questions[semester] = self.exam_questions
            if semester in self.test_semester:
                self.test_questions[semester] = self.exam_questions

    def get_question_instances_per_semester(self):
        self.exam_instances_semester = {}
        all_semester_folders = self.exam_instances_per_semester()
        for semester_folders in all_semester_folders:
            for semester, folder in semester_folders.items():
                if semester in self.train_semester or semester in self.test_semester:
                    exam_instances_per_semester = self.get_all_exam_instances_per_semester(folder)
                    if exam_instances_per_semester:
                        self.get_exam_instances_per_semester(exam_instances_per_semester, semester)

    def write_questions(self):
        questions_train = ""
        questions_test = ""
        for semester, exams in self.train_questions.items():
            for exam, exam_questions in exams.items():
                questions_train = questions_train + "\nsemester: %s, exam:%s \n" %(semester, exam)
                questions_train = questions_train + "\n".join(exam_questions) + "\n****************************"
        with open("train_questions.txt", "w") as file:
            file.write(questions_train.strip())
        for semester, exams in self.test_questions.items():
            for exam, exam_questions in exams.items():
                questions_test = questions_test + "\nsemester: %s, exam:%s \n" %(semester, exam)
                questions_test = questions_test + "\n".join(exam_questions) + "\n****************************"
        with open("test_questions.txt", "w") as file:
            file.write(questions_test.strip())
    
    def get_exam_questions(self):
        self.get_question_instances_per_semester()
        self.get_all_questions()
        self.write_questions()
