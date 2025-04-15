import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

if os.path.isdir("matched_questions"):
    files = os.listdir("matched_questions")
    values = []
    for file in files:
        names = file.split("_")
        semester = names[0]
        exam = names[1]
        question_count = int(names[2])
        sim_type = names[3].split(".")[0]
        file_path = os.path.join("matched_questions", file)
        with open(file_path, 'r') as f:
            data = f.read()
            data_list = data.split("\n")
            count = [_data for _data in data_list if len(_data) > 0]
            values.append([semester, exam, question_count, len(count), sim_type])
    df = pd.DataFrame(values, columns=['Semester', 'Exam', 'TotalQuestion', 'QuestionCount', "Type"])
    df['Accuracy'] = df['QuestionCount'] / df['TotalQuestion']
    df_st = df[df['Type'] == "SentenceTransformer"]
    print("Total Accuracy with Sentence Transformer: %f" %(df_st['QuestionCount'].sum()/df_st['TotalQuestion'].sum()))
    df_faiss = df[df['Type'] == "FAISS"]
    print("Total Accuracy with FAISS: %f" %(df_faiss['QuestionCount'].sum()/df_faiss['TotalQuestion'].sum()))
    sns.barplot(df, x="Exam", y="Accuracy", hue="Type")
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15))
    plt.savefig("Analysis.pdf")
