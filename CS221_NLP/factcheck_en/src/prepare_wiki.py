import os
import json
import pandas as pd
from tqdm.auto import tqdm

input_dir = os.path.join(".","fever_wiki", "wiki-pages")

pyserini_corpara_dir = os.path.join(".", "fever_wiki", "corpora")

doc_id = 0

for file_name in tqdm(sorted(os.listdir(input_dir))):

    input_file_path = os.path.join(input_dir, file_name)

    pyserini_corpara_file_path = os.path.join(pyserini_corpara_dir, file_name)

    if not os.path.isfile(input_file_path):
        continue

    data = pd.read_json(path_or_buf=input_file_path, lines=True)

    # create corpara for pyserini
    pyserini_corpara = pd.DataFrame()

    pyserini_corpara["id"] = data.index + doc_id

    # pyserini_corpara["contents"] = data.agg('{0[id]}\t{0[text]}'.format, axis=1).apply(lambda text: text.replace('_', ' '))

    pyserini_corpara["contents"] = data["text"]
    pyserini_corpara["title"] = data["id"]

    # pyserini_corpara["text"] = data["lines"]

    pyserini_corpara.to_json(pyserini_corpara_file_path, orient='records', lines=True)

    doc_id = doc_id + data.shape[0]

