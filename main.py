import openai
import os
import sys
import nltk
from nltk.corpus import stopwords

from dotenv import load_dotenv
import pandas as pd

from recommend_questions import QuestionRecommendation
from exam_questions import ExamQuestions
from similar_question import SimilarQuestion
from analyze_results import AnalyzeResults
from analyze_results_st import AnalyzeResultsSentenceTransformer

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

nltk.download('punkt_tab')
nltk.download('stopwords')

def main():
    if(command == "--getQuestions") or (command == "--all"):
        exam_questions = ExamQuestions(instance_link, question_link, train_semesters, test_semesters)
        exam_questions.get_exam_questions()
        print("Completed!")
    if(command == "--getSimilarQuestions") or (command == "--all"):
        similar_questions = SimilarQuestion(API_KEY, train_semesters[-1])
        similar_questions.get_similar_questions()
        print("Completed!")
    if(command == "--recommendQuestions") or (command == "--all"):
        recommend_questions = QuestionRecommendation(API_KEY)
        recommend_questions.recommend_questions()
        print("New question generation completed!")
    if(command == "--analyze") or (command == "--all"): 
        analyze_results = AnalyzeResults(API_KEY)
        analyze_results.analyze()
        print("Analyze Completed!")

if __name__ == "__main__":
    main()
