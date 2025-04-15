import openai
import os
import sys

from dotenv import load_dotenv
import pandas as pd

from generate_questions import QuestionGeneration
from exam_questions import ExamQuestions
from similar_question import SimilarQuestion
from analyze_results import AnalyzeResults

load_dotenv()
API_KEY = os.getenv("API_KEY")
command = sys.argv[-1]
instance_link = os.getenv("INSTANCE_LINK")
question_link = os.getenv("QUESTION_LINK")
train_semesters = [
    "Fa19", "Fa20", "Fa21", "Fa22", "Fa23",
    "Sp20", "Sp21", "Sp22", "Sp23", "Sp24"
]
test_semesters = ["Fa24"]
exams = ["exam0", "exam1", "exam2", "exam3"]

def main():
    if(command == "--getQuestions"):
        exam_questions = ExamQuestions(instance_link, question_link, train_semesters, test_semesters)
        exam_questions.get_exam_questions()
        print("Completed!")
    if(command == "--getSimilarQuestions"):
        similar_questions = SimilarQuestion(API_KEY, train_semesters[-1])
        similar_questions.get_similar_questions()
        print("Completed!")
    if(command == "--generateQuestions"):
        generate_questions = QuestionGeneration(API_KEY)
        generate_questions.generate_questions()
        print("New question generation completed!")
    if(command == "--analyze"):
        analyze_results = AnalyzeResults(API_KEY)
        analyze_results.analyze()
        print("Analyze Completed!")

if __name__ == "__main__":
    main()
