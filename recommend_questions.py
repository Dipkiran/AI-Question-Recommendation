import openai
import os
import time
import json
import tiktoken
from tqdm import tqdm

class QuestionRecommendation:
    def __init__(self, API_KEY):
        openai.api_key = API_KEY

    def get_input_data(self, questions):
        question_list = questions.split("\n")
        question_list = question_list[1:]
        all_questions = {}
        tokens = 0
        for question in question_list:
            if len(question) > 0:
                question = json.loads(question)
                matched_question = question['matched_question']
                if not(all_questions.get(matched_question)):
                    all_questions[matched_question] = []
                if (question['distance']) > 0 and (question['distance']) < 0.2:
                    sim_questions = all_questions[matched_question]
                    encoding = tiktoken.encoding_for_model("gpt-4o")
                    tokens = encoding.encode("".join(sim_questions))
                    if len(tokens) < 8000:
                        sim_questions.append(question['ques'])
                        all_questions[matched_question] = sim_questions
        input_questions = []
        for question, similar_questions in all_questions.items():
            similar_questions.append(question)
            input_questions.append(similar_questions)
        return input_questions

    def predict_question(self, input_data):
        prompt = f"""
        You are a teacher of the Introduction to Programming course in Computer Science. Your job is to generate an exam question based on given questions:
        {input_data}
        Recommend only 1 question that follow the same structure and topic distribution.
        Ensure that the questions maintain logical flow and do not repeat exactly. Do not give answers or any feedback.
        """
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    def recommend_questions(self):
        ques_folder = "similar_questions"
        new_question_folder = "new_questions"
        if not os.path.isdir(new_question_folder):
            os.mkdir(new_question_folder)
        folders = os.listdir(ques_folder)
        for folder in folders:
            exam_title = folder.split(".")[0]
            question_path = os.path.join(ques_folder, folder)
            with open(question_path, "r") as file:
                questions = file.read()
                input_questions_list = self.get_input_data(questions)
                new_questions = []
                for input_questions in tqdm(input_questions_list):
                    new_question = self.predict_question(input_questions)
                    new_questions.append(new_question)
                    new_questions.append("***************************************")
                    time.sleep(5)
                question_file_loc = "%s.txt" %(exam_title)
                question_file_path = os.path.join(new_question_folder, question_file_loc)
                with open(question_file_path, 'w') as f:
                    for questions in new_questions:
                        f.write(f"{questions}\n")
