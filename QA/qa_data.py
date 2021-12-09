import csv
from collections import defaultdict
import pandas as pd
import numpy as np
import re
from sklearn.model_selection import train_test_split

import pytorch_lightning as pl
from pytorch_lightning.callbacks import ModelCheckpoint
from model import QADataset, DataModule, QAModel

''' first read data from file '''
questions = list() # list of questions
answers = list() # list of answers the same order as questions
contexts = defaultdict(lambda : list()) # q : list of contexts

with open("question_answer.txt", 'r+') as qa_file:
    for line in qa_file:
        question, answer = line.split('|')
        questions.append(question.strip())
        answers.append(answer.strip())

with open("qa_query_docs.csv", 'r+') as data_file:
    data_reader = csv.DictReader(data_file)
    for row in data_reader:
        question, context = row["Query"], row["relevant_transcript"]
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
# print(df.head(5))

''' create dataset for training '''
# qa_dataset = QADataset(df)
# for data in qa_dataset:
#     print("Question: ", data['question'])
#     print("Answer text: ", data['answer_text'])
#     print("Input_ids: ", data['input_ids'][:10])
#     print("Labels: ", data['labels'][:10])
#     break 

train_df, val_df = train_test_split(df, test_size=3)

BATCH_SIZE = 8
EPOCHS = 2
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

''' evaluations '''
trained_model = QAModel.load_from_checkpoint("checkpoints/best-checkpoint.ckpt")
trained_model.freeze() #


sample_question = val_df.iloc[0]
print(sample_question["question"])
print(sample_question["answer_text"])  # Label Answer
predicted_answer = generate_answer(sample_question, trained_model)  # Predicted answer
print(predicted_answer)
