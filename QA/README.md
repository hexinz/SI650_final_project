### Training Data:

We designed 130 Q&A pairs in total. The questions are designed so that each can be answered by context of one line in a particular transcript. While this seems limiting, it is quite necessary due to the huge workload of data annotation and limited labeled data resources.

### Training Process:

The T5 model is initially pretrained on the C4 dataset. Since our data is very limited, it is lucrative to first continue pretrain on a general Q&A dataset, and finally finetune on our own TV-domain Q&A pairs. Specifically, I chose the `triviaQA` dataset because it has the same input format of `(question, context, answer)` triples. We hope the model to learn general natural language questions, which is knowledge that could transfer to our specific domain data.

```bash
Testing: 100%|█████████████████████████████████| 10/10 [00:01<00:00,  7.26it/s]
--------------------------------------------------------------------------------
DATALOADER:0 TEST RESULTS
{'test_loss': 1.187434434890747}
```

### Train Test Split

We adopted the `train_test_split` method provided in the scikit-learn package. We set the validation/test set to be 10% of the overall data. The `random_state` is not fixed during finetuning, but is fixed in the final test stage to ensure reproducibility.

### Test performance:

Accuracy = $11/13\approx84\%$

```bash
$ python predict.py 2>/dev/null
---------------------------------------------
Test Question:           Where did Penny and Leonard marry
Correct Answer:          Las Vegas
Predicted Answer:        Las Vegas
---------------------------------------------
Test Question:           Who had food poisoning
Correct Answer:          Howard
Predicted Answer:        Howard
---------------------------------------------
Test Question:           Who gets the MacArthur Fellowship
Correct Answer:          Bert
Predicted Answer:        Bert
---------------------------------------------
Test Question:           Sheldon is pathologically afraid of what
Correct Answer:          birds
Predicted Answer:        birds
---------------------------------------------
Test Question:           Who is going to jail for tax fraud
Correct Answer:          Howard
Predicted Answer:        Howard
---------------------------------------------
Test Question:           Is the new assistant named Alex is a boy or girl
Correct Answer:          girl
Predicted Answer:        girl
---------------------------------------------
Test Question:           What was the air force interested in
Correct Answer:          quantam gyroscope
Predicted Answer:        Quantum Leap
---------------------------------------------
Test Question:           Who thought the scavenger hunt is a interesting social experiment
Correct Answer:          Howard
Predicted Answer:        Howard
---------------------------------------------
Test Question:           Who is pathologically afraid of birds
Correct Answer:          Sheldon
Predicted Answer:        Sheldon
---------------------------------------------
Test Question:           The new assistant named Alex is a boy or girl
Correct Answer:          girl
Predicted Answer:        girl
---------------------------------------------
Test Question:           Who wanted to live on Mars
Correct Answer:          Sheldon
Predicted Answer:        Leonard
---------------------------------------------
Test Question:           What did the air force contact Howard about quantam what
Correct Answer:          quantam gyroscope
Predicted Answer:        quantam gyroscope
---------------------------------------------
Test Question:           Who does not have a driving license
Correct Answer:          Sheldon
Predicted Answer:        Sheldon
```
