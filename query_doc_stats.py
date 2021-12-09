from collections import defaultdict, Counter
from matplotlib import pyplot as plt
import csv

with open("relevant_document_new.csv", 'r+', encoding="utf-8") as fin:
    reader = csv.DictReader(fin, delimiter=',')
    queries = defaultdict(lambda : list())
    for row in reader:
        if row['relevance_score'] is None:
            continue

        query = row['Query']
        score = int(row['relevance_score'])

        queries[query].append(score)

query_keys = list(queries.keys())

overall = Counter()

print(len(queries))
fig, axs = plt.subplots(6, 5)
fig.set_size_inches(12, 10)
for i in range(6):
    for j in range(5):
        query = query_keys[5*i+j]
        axs[i, j].hist(queries[query], bins=3)
        overall.update(queries[query])

#fig.xlabel('relevance score')
#fig.ylabel('number of documents')
plt.savefig("query_doc_stats.png")
print(overall.most_common(3))