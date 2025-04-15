import os
import openai
from sentence_transformers import SentenceTransformer, util
from tqdm import tqdm

class AnalyzeResultsSentenceTransformer:
    def __init__(self, API_KEY):
        openai.api_key = API_KEY

    def find_similarity(self, semester, exam, questions):
        predicted_questions_dir = "new_questions"
        exam_path = "%s.txt" %(exam)
        predicted_questions_path = os.path.join(predicted_questions_dir, exam_path)
        matched_questions = []
        model = SentenceTransformer('all-MiniLM-L6-v2')
        with open (predicted_questions_path) as file:
            predicted_questions = file.read()
            predicted_question_list = predicted_questions.split("***************************************")
            embeddings_q = model.encode(questions, convert_to_tensor=True)
            embeddings_pq = model.encode(predicted_question_list, convert_to_tensor=True)
            cos_sim = util.cos_sim(embeddings_q, embeddings_pq)
            for i, question in tqdm(enumerate(questions)):
                best_match_idx = cos_sim[i].argmax()
                best_score = cos_sim[i][best_match_idx].item()
                if best_score > 0.8:
                    matched_questions.append([question, predicted_question_list[best_match_idx], float(best_score)])

            file_path = "%s_%s_%s_SentenceTransformer.txt" %(semester, exam, str(len(questions)))
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
                    questions = [question for question in questions]
                    self.find_similarity(semester, exam, questions)
