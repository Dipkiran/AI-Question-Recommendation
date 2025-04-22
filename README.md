Steps to run the script: (You can run step 1 to 5 using python main.py --all)

1) First we need to get the questions from the PrairieLearn for our analysis. Run using the command:
-> python3 main.py --getQuestions

2) After this, we group the similar questions by passing the argument --getSimilarQuestions.
-> python main.py --getSimilarQuestions

3) We then pass the similar questions to the ChatGPT which will recommend a question for a set of questions.
-> python main.py --generateQuestions

4) --analyze command find the similar questions using FAISS with threshold 0.7.
-> python main.py --analyze

5)To run analysis after removing stop words use --analyzeNoStopWords.
-> python main.py --analyzeNoStopWords

5) Run visualize_results.py to generate the visualization of data.
-> python visualize_results.py