import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

if os.path.isdir("matched_questions"):
    files = os.listdir("matched_questions")
    values = []
    for file in files:
        semester = file.split("_")[0]
        exam = file.split("_")[1]
        question_count = int(file.split("_")[2].split(".")[0])
        file_path = os.path.join("matched_questions", file)
        with open(file_path, 'r') as f:
            data = f.read()
            data_list = data.split("\n")
            count = [_data for _data in data_list if len(_data) > 0]
            values.append([semester, exam, question_count, len(count)])
    df = pd.DataFrame(values, columns=['Semester', 'Exam', 'TotalQuestion', 'QuestionCount'])
    df['Accuracy'] = df['QuestionCount'] / df['TotalQuestion']
    print("Total Accuracy: %f" %(df['QuestionCount'].sum()/df['TotalQuestion'].sum()))
    sns.barplot(df, x="Exam", y="Accuracy")
    plt.savefig("Analysis.pdf")
