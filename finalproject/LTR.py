#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pyterrier as pt


# In[2]:


if not pt.started():
    pt.init()


# In[3]:


import pandas as pd

import jsonlines
all_documents=[]
with open("documents.jsonl", "r+", encoding="utf8") as f:
    for item in jsonlines.Reader(f):
        all_documents.append(item)


# In[4]:


import json
all_transcript=[]
for i in range(len(all_documents)):
    try:
    
        all_transcript.append(dict({'id':all_documents[i]['id'],'contents':

                                      '('+str(json.loads(all_documents[i]['contents'])['series'])+' '+ str(json.loads(all_documents[i]['contents'])['episode'])+') '
                                      +json.loads(all_documents[i]['contents'])['actor']+': '+json.loads(all_documents[i]['contents'])['line']+
                                      '('+str(json.loads(all_documents[i+1]['contents'])['series'])+' '+ str(json.loads(all_documents[i+1]['contents'])['episode'])+') '
                                      +json.loads(all_documents[i+1]['contents'])['actor']+': '+json.loads(all_documents[i+1]['contents'])['line'] }))




                                  
                                  
                                 
    except:
        all_transcript.append(dict({'id':all_documents[i]['id'],'contents':
                                  '('+str(json.loads(all_documents[i]['contents'])['series'])+' '+ str(json.loads(all_documents[i]['contents'])['episode'])+') '
                                  +json.loads(all_documents[i]['contents'])['actor']+': '+json.loads(all_documents[i]['contents'])['line']
        }))



    
      
    


# In[5]:


doc_id=list(all_transcript[i]['id'] for i in range(len(all_transcript)))
context=list(str(all_transcript[i]['contents'] )for i in range(len(all_transcript)))


# In[6]:


transcript_df=pd.DataFrame({'docno': doc_id, 'text':context})


# In[7]:


#index_dir = './transcriptedocs_index'
#indexer = pt.DFIndexer(index_dir, overwrite=True, blocks=True)
#index_ref = indexer.index(transcript_df["text"], transcript_df["docno"])
#index_ref.toString()


# In[8]:


index = pt.IndexFactory.of('./transcriptedocs_index/data.properties')


# In[9]:


all_query=pd.read_csv("query_new_0-30.csv")
all_query.columns=['qid','query']
all_query['qid']=list(str(all_query['qid'][i]) for i in range(len(all_query)))


# In[10]:


results=pd.read_csv('new_qa_relevance_0-30_1500.csv')
results.columns=['index','q_id','q_text','trans_id','trans_text','label']
qrels=pd.DataFrame({'qid':list(str(results['q_id'][i])for i in range(len(results))),'docno':list(str(results['trans_id'][i])for i in range(len(results))),'label':list(float(results['label'][i]) for i in range(len(results)))})



# In[11]:

SEED=42

from sklearn.model_selection import train_test_split

tr_va_topics, test_topics = train_test_split(all_query, test_size=5, random_state=SEED)
train_topics, valid_topics =  train_test_split(tr_va_topics, test_size=5, random_state=SEED)


# In[13]:


sdm = pt.rewrite.SequentialDependence()
bm25 = pt.BatchRetrieve(index, wmodel="BM25")
pipeline1 = sdm >> bm25
bo1 = pt.rewrite.Bo1QueryExpansion(index)
pipeline2 =  bm25 >> bo1 >> bm25
tf= pt.BatchRetrieve(index,  wmodel="Tf")

pl2 = pt.BatchRetrieve(index, wmodel="PL2" )
DPH= pt.BatchRetrieve( index, wmodel="DPH")
DLM  = pt.BatchRetrieve(index, wmodel="DirichletLM")
RANK_CUTOFF=15
ltr_feats1 = (bm25 % RANK_CUTOFF) >> (
    pt.transformer.IdentityTransformer()
    **
    (sdm >> bm25)
    **
    (bm25>>bo1>>bm25)
    **
    pt.BatchRetrieve(index, wmodel="CoordinateMatch")
    **
    tf
    
    

  
)

# for reference, lets record the feature names here too
fnames=["BM25", "SDM","bo1","coordinateMatch","tf"]


# In[14]:


import fastrank

train_request = fastrank.TrainRequest.coordinate_ascent()

params = train_request.params
params.init_random = True
params.normalize = True
params.seed = 1234567

ca_pipe = ltr_feats1 >> pt.ltr.apply_learned_model(train_request, form='fastrank')

ca_pipe.fit(train_topics, qrels)


# In[15]:



def BM25(query):
    results = []
    document_id_temp=[]
    document_text=[]
    doc_number=bm25.search(query)['docno'][0:10]
    for j in doc_number:
        document_id_temp.append(int(j))
        document_text.append(transcript_df.iloc[int(j)]['text'])
        results.append([int(j),transcript_df.iloc[int(j)]['text']])
    relevant_df=pd.DataFrame({'transcript_id':document_id_temp, 'transcript':document_text})
    return results
    
    


# In[16]:


def FastRank(query):
    results=[]
    document_id_temp=[]
    document_text=[]
    doc_number=ca_pipe.search(query)['docno'][0:10]
    for j in doc_number:
        document_id_temp.append(int(j))
        document_text.append(transcript_df.iloc[int(j)]['text'])
        results.append([int(j),transcript_df.iloc[int(j)]['text']])
    relevant_df=pd.DataFrame({'transcript_id':document_id_temp, 'transcript':document_text})
    return results
    


# In[18]:
print(FastRank('Sheldon Hello'))





# In[ ]:




