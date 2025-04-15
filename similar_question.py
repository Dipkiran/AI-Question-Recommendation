import openai
import faiss
import json
import os
from tqdm import tqdm
import numpy as np

class SimilarQuestion:
    def __init__(self, API_KEY, reference_exam):
        openai.api_key = API_KEY
        self.reference_exam = reference_exam
        self.train_data = {}
        self.group_input_questions = {}

    def read_train_questions(self):
        with open("train_questions.txt", "r") as file:
            data = file.read()
            data_list = data.split("****************************")
            for _data in data_list:
                _data = _data.strip()
                exam_semester = _data.split("\n")[0]
                if exam_semester:
                    semester = exam_semester.split(",")[0].split(":")[-1].strip()
                    exam = exam_semester.split(",")[1].split(":")[-1].strip()
                    if self.train_data.get(exam):
                        semester_data = self.train_data[exam]
                        if semester == self.reference_exam:
                            semester_data.insert(0, {'questions': _data.split("\n")[1:]})
                        else:
                            semester_data.append({'questions': _data.split("\n")[1:]})
                        self.train_data[exam] = semester_data
                    else:
                        self.train_data[exam] = [{'questions': _data.split("\n")[1:]}]
    
    def get_embedding(self, text, model="text-embedding-ada-002"):
        response = openai.embeddings.create(input=[text], model=model)
        return np.array(response.data[0].embedding, dtype=np.float32)
    
    def get_similar_question(self, questions, index, ref_ques, exam_type):
        for ques in questions:
            question_embedding = self.get_embedding(ques).reshape(1, -1)
            faiss.normalize_L2(question_embedding)
            D, I = index.search(question_embedding, k=1)
            matched_question = ref_ques[I[0][0]]
            similar_question = json.dumps({
                "ques": ques,
                "matched_question": matched_question,
                "distance": float(D[0][0])
            })
            if self.group_input_questions.get(exam_type):
                grouped_questions = self.group_input_questions[exam_type]
                grouped_questions.append(similar_question)
                self.group_input_questions[exam_type] = grouped_questions
            else:
                self.group_input_questions[exam_type] = [similar_question]

    def generate_reference_embedding(self, ref_exam):
        questions = ref_exam
        desc = "Generating Embedding"
        embedding = np.array(
            [self.get_embedding(q) for q in tqdm(questions, desc=desc)]
        )
        dimension = embedding.shape[1]
        index = faiss.IndexFlatL2(dimension)
        faiss.normalize_L2(embedding)
        index.add(embedding)
        return index
    
    def similar_questions_per_exam(self, exam):
        exam_data = self.train_data[exam]
        ref_exam = exam_data[0]['questions']
        index = self.generate_reference_embedding(ref_exam)
        print("Finding Similar Questions for %s" %(exam))
        for i in tqdm(range(1, len(exam_data))):
            semester_data = exam_data[i]['questions']
            self.get_similar_question(semester_data, index, ref_exam, exam)
        filename = "similar_questions/%s.txt" %(exam)
        with open(filename, 'w') as f:
            for exam, ques_list in self.group_input_questions.items():
                f.write(f"{exam}**************\n")
                for ques in ques_list:
                    f.write(f"{ques}\n")

    def find_similar_questions(self):
        exams = list(self.train_data.keys())
        for exam in exams:
            self.similar_questions_per_exam(exam)
            self.group_input_questions = {}

    def get_similar_questions(self):
        self.read_train_questions()
        if not os.path.isdir("similar_questions"):
            os.mkdir("similar_questions")
        self.find_similar_questions()
        print("Completed!")
        