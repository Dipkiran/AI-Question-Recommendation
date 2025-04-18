Steps to run the script:

1) First we need to get the questions from the PrairieLearn for our analysis. Run using the command:
-> python3 main.py --getQuestions

2) After this, we group the similar questions by passing the argument --getSimilarQuestions.
-> python main.py --getSimilarQuestions

3) We then pass the similar questions to the ChatGPT which will recommend a question for a set of questions.
-> python main.py --generateQuestions

4) --analyze command find the similar questions using FAISS with threshold 0.8.
-> python main.py --analyze

5) Run visualize_results.py to generate the visualization of data.