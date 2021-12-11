import os
import re
import csv
import pandas as pd
import numpy as np
from collections import defaultdict
import pytorch_lightning as pl
from sklearn.model_selection import train_test_split
from pytorch_lightning.callbacks import ModelCheckpoint
from qa_model import QADataset, DataModule, QAModel
from qa_model import generate_answer
import sys

''' incorporate into final project '''

def predicted_answer(checkpoint, df, verbose=False):
    '''
    :param: checkpoint: a string containing the checkpoint_path to be loaded
    :param: df: the dataframe containing 'question' and 'content' (and optionally 'answer_text') column
    :returns: answers: a list of strings containing the predicted answers, the list have same length as df
    '''
    trained_model = QAModel.load_from_checkpoint(checkpoint)
    trained_model.freeze() #
    answers = list()
    for i in range(len(df)):
        try: 
            sample_question = df.iloc[i]
            predicted_answer = generate_answer(sample_question, trained_model)  # Predicted answer
            if verbose:
                print('---------------------------------------------')
                print("Test Question:\t\t", sample_question["question"])
                print("Correct Answer:\t\t", sample_question["answer_text"])  # Label Answer
                print("Predicted Answer:\t", predicted_answer)
            answers.append(predicted_answer)
        except:
            answers.append("*")
            continue
    return answers

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python test.py [path_to_checkpoint] [path_to_csv]")
        print("\t the csv should contain the dataframe holding 'question' and 'context' column")
        exit(1)
    
    checkpoint = sys.argv[1]
    df = pd.read_csv(sys.argv[2])
    _, df = train_test_split(df, test_size=0.15, random_state=0)
    predicted_answer(checkpoint, df, verbose=True)