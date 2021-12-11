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

''' evaluations '''
trained_model = QAModel.load_from_checkpoint("checkpoints/best-checkpoint-v4.ckpt")
trained_model.freeze() #

qa_data_file = 'qa_data.csv'
df = pd.read_csv(qa_data_file)
train_df, val_df = train_test_split(df, test_size=0.15, random_state=0)

for i in range(len(val_df)):
    try: 
        sample_question = val_df.iloc[i]
        predicted_answer = generate_answer(sample_question, trained_model)  # Predicted answer
        print('---------------------------------------------')
        print("Test Question:\t\t", sample_question["question"])
        print("Correct Answer:\t\t", sample_question["answer_text"])  # Label Answer
        print("Predicted Answer:\t", predicted_answer)
    except:
        continue
