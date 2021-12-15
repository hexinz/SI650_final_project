

qa_pair = {'Where did Penny and Leonard marry':'Las Vegas',
           'Who had food poisoning':'Howard',
           'Who gets the MacArthur Fellowship':'Bert',
           'Sheldon is pathologically afraid of what':'birds',
           'Who is going to jail for tax fraud':'Howard',
           'Is the new assistant named Alex is a boy or girl':'girl',
           'What was the air force interested in':'Quantum Leap',
           'Who thought the scavenger hunt is a interesting social experiment':'Howard',
           'Who is pathologically afraid of birds':'Sheldon',
           'The new assistant named Alex is a boy or girl':'girl',
           'Who wanted to live on Mars':'Sheldon',
           'What did the air force contact Howard about quantam what':'quantam gyroscope',
           'Who does not have a driving license': 'Sheldon'
           }

def get_answer(query):
    print(query)
    return qa_pair.get(query,0)