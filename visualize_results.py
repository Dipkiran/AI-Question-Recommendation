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
    df['Accuracy'] = df['Accuracy'].round(2)
    df['StopWords'] = False
    df.loc[df['Type']=="StopWords", 'StopWords'] = True
    df_nst = df[df['StopWords'] == False]
    print("Total Accuracy with: %f" %(df_nst['QuestionCount'].sum()/df_nst['TotalQuestion'].sum()))
    df_faiss = df[df['StopWords'] == True]
    print("Total Accuracy with StopWords: %f" %(df_faiss['QuestionCount'].sum()/df_faiss['TotalQuestion'].sum()))
    print(df)
    ax = sns.barplot(df, x="Exam", y="Accuracy", hue="StopWords")
    for i in ax.containers:
        ax.bar_label(i,)
    plt.legend(title= 'Stop Words', loc='upper center', bbox_to_anchor=(0.5, 1.17), ncol=2)
    plt.savefig("Analysis.pdf")
