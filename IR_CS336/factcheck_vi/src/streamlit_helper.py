import streamlit as st
from service_streamer import ThreadedStreamer
from model import model_wrapper
import os
import json
import pandas as pd
import spacy
import json

from pyserini.search.lucene import LuceneSearcher
from pyserini.search import FaissSearcher

import torch
import argparse


@st.cache_resource
def get_split_sents():
    nlp = spacy.load("en_core_web_trf")

    @st.cache_data
    def split_sents(text):
        text = text.replace("\n", " ")
        sents = [str(sent) for sent in nlp(text).sents]
        sents = [s for s in sents if s not in ["\n", '']]
        return sents
    
    return split_sents

@st.cache_resource
def get_predict_fc(checkpoint_path, device, batch_size):
    mo = model_wrapper(
        checkpoint_path=checkpoint_path,
        device=device,
        strict=False
    )
    streamer = ThreadedStreamer(mo.predict, batch_size=batch_size, max_latency=0.1)

    @st.cache_data
    def predict_fc(sents, claim):
        tmp = {
            "claim": claim,
            "sentences":sents
        }
        outputs = streamer.predict([tmp])
        return outputs[0]
        
    return predict_fc

@st.cache_resource
def get_search_fc(index_dir, raw_doc_index):
    searcher = FaissSearcher(
        index_dir,
        query_encoder="bkai-foundation-models/vietnamese-bi-encoder"
    )

    docs = LuceneSearcher(raw_doc_index)

    @st.cache_data
    def search_doc(query):
        hits = searcher.search(query)

        return [json.loads(docs.doc(h.docid).raw()) for h in hits]
    
    return search_doc

@st.cache_data
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cuda", action='store_true', help="use cuda if available")
    parser.add_argument("--checkpoint_path", type=str,help="path to model checkpoint", default="checkpoints/fever_sci.ckpt")
    parser.add_argument("--index_dir", type=str,help="path to index", default="indexes/fever_wiki")
    parser.add_argument("--raw_doc_index", type=str,help="path to index", default="indexes/raw")
    parser.add_argument("--batch_size", type=int,default=1)
    args = parser.parse_args()

    args = vars(args)

    args["device"] = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    return args

