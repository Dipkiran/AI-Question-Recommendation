import os
import sys
import openai
import faiss
from tqdm import tqdm
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize

class AnalyzeResultsRemoveStopWords:
    def __init__(self, API_KEY, stopwords):
        openai.api_key = API_KEY
        self.stopwords = stopwords
    
    def get_embedding(self, text, model="text-embedding-ada-002"):
        response = openai.embeddings.create(input=[text], model=model)
        return np.array(response.data[0].embedding, dtype=np.float32)
    
    def remove_stopwords(self, all_questions):
        questions = []
        for question in all_questions:
            words = word_tokenize(question.lower())
            ques = [word for word in words if word not in self.stopwords]
            if len(ques) > 0:
                questions.append(" ".join(ques))
        return questions

    def find_similarity(self, semester, exam, questions):
        predicted_questions_dir = "new_questions"
        exam_path = "%s.txt" %(exam)
        predicted_questions_path = os.path.join(predicted_questions_dir, exam_path)
        matched_questions = []
        with open (predicted_questions_path) as file:
            predicted_questions = file.read()
            predicted_question_list = predicted_questions.split("***************************************")
            predicted_question_list = self.remove_stopwords(predicted_question_list)
            description = "Generating embedding for %s of %s" %(exam, semester)
            embedding = np.array(
                [self.get_embedding(q) for q in tqdm(predicted_question_list, desc=description)]
            )
            dimension = embedding.shape[1]
            index = faiss.IndexFlatL2(dimension)
            faiss.normalize_L2(embedding)
            index.add(embedding)
            for question in tqdm(questions, desc="Matching questions"):
                question_embedding = self.get_embedding(question).reshape(1, -1)
                faiss.normalize_L2(question_embedding)
                D, I = index.search(question_embedding, k=1)
                matched_question = predicted_question_list[I[0][0]]
                if float(D[0][0]) <= 0.3:
                    matched_questions.append([question, matched_question, float(D[0][0])]))])
            file_path = "%s_%s_%s_NoStopWords.txt" %(semester, exam, str(len(questions)))
            matched_file_path = os.path.join("matched_questions", file_path)
            with open(matched_file_path, 'w') as f:
                for m_question in matched_questions:
                    f.write(f"{m_question}\n")

    def analyze(self):
        if not os.path.isdir("matched_questions"):
            os.mkdir("matched_questions")
        with open("test_questions.txt") as file:
            data = file.read()
            data_list = data.split("****************************")
            for _data in data_list:
                _data = _data.strip()
                exam_semester = _data.split("\n")[0]
                if exam_semester:
                    semester = exam_semester.split(",")[0].split(":")[-1].strip()
                    exam = exam_semester.split(",")[1].split(":")[-1].strip()
                    questions = _data.split("\n")[1:]
                    questions = self.remove_stopwords(questions)
                    self.find_similarity(semester, exam, questions)
