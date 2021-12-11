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

''' first read data from file '''

qa_data_file = 'qa_data.csv'
if not os.path.exists(qa_data_file):
    questions = list() # list of questions
    answers = list() # list of answers the same order as questions
    contexts = defaultdict(lambda : list()) # q : list of contexts

    with open("question_answer.txt", 'r+') as qa_file:
        for line in qa_file:
            question, answer = line.split('|')
            questions.append(question.strip())
            answers.append(answer.strip())

    with open("qa_relevance.csv", 'r+') as data_file:
        data_reader = csv.DictReader(data_file)
        for row in data_reader:
            question, context = row["query"], row["transcript"]
            if len(question) == 0:
                continue
            regex = r"^\(.+\)(.+)"
            match = re.findall(regex, context)
            context = match[0].strip()
            contexts[question].append(context)

    data = list()
    for i, question in enumerate(questions):
        context = " ".join(c for c in contexts[question])
        data.append([question, context, answers[i]])

    df = pd.DataFrame(np.array(data))
    df.columns = ['question', 'context', 'answer_text']
    df.to_csv(qa_data_file, index=False)
else:
    df = pd.read_csv(qa_data_file)

''' create dataset and set training parameters '''

BATCH_SIZE = 8
EPOCHS = 50
VAL_SIZE = 0.1

train_df, val_df = train_test_split(df, test_size=VAL_SIZE)
data_module = DataModule(train_df, val_df, batch_size=BATCH_SIZE)
data_module.setup() 

''' define models '''
model = QAModel()
checkpoint_callback = ModelCheckpoint(
    dirpath="checkpoints",
    filename="best-checkpoint",
    save_top_k=1,
    verbose=True,
    monitor="val_loss",
    mode="min"
)
trainer = pl.Trainer(
    checkpoint_callback=checkpoint_callback,
    max_epochs=EPOCHS,
    gpus=1,
    progress_bar_refresh_rate = 30
) 

''' start finetune '''
trainer.fit(model, data_module)
trainer.test() # evaluate the model according to the last checkpoint
