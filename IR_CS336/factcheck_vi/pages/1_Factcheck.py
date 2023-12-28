import sys
sys.path.append("./src")

import streamlit as st
from annotated_text import annotated_text
from src.streamlit_helper import get_args, get_predict_fc, get_search_fc

import pandas as pd

import random
import numpy as np

from underthesea import sent_tokenize, word_tokenize

###############################################
# https://discuss.streamlit.io/t/problem-share-session-state-on-multipages/27755/8
# https://stackoverflow.com/questions/74968179/session-state-is-reset-in-streamlit-multipage-app
for k, v in st.session_state.to_dict().items():
    st.session_state[k] = v
###############################################

st.set_page_config(layout="wide")


args = get_args()

predict_fc = get_predict_fc(
    checkpoint_path = args["checkpoint_path"], 
    device=args["device"], 
    batch_size=args["batch_size"]
)
search_fc = get_search_fc(
    index_dir=args["index_dir"],
    raw_doc_index=args["raw_doc_index"]
    )

if "claim" not in st.session_state:
    st.session_state["claim"] = ""

if "fc_annotated_re" not in st.session_state:
    st.session_state["fc_annotated_re"] = []

if "selection_table" not in st.session_state:
    st.session_state["selection_table"] = []

if "annotated_res" not in st.session_state:
    st.session_state["annotated_res"] = []


def get_sample_query():
    queries = [
        "Đặng Anh Đào chưa mất.",
        "chợ Gò Vấp có từ hơn 100 năm trước",
        "Bảo tàng Mỹ thuật TP HCM là một trong 31 di tích văn hóa, lịch sử",
        "Bảo tàng Mỹ thuật TP HCM thu hút hơn 300.000 lượt khách mỗi năm"
    ]

    st.session_state.claim = random.choice(queries)

def dataframe_with_selections(df):
    df_with_selections = df.copy()
    df_with_selections.insert(0, "Select", False)
    df_with_selections.loc[0,"Select"] = True
    edited_df = st.data_editor(
        df_with_selections,
        hide_index=True,
        column_config={"Select": st.column_config.CheckboxColumn(required=True)},
        disabled=df.columns,
    )
    selected_indices = list(np.where(edited_df.Select)[0])
    return selected_indices



def factcheck_button():
    st.session_state.annotated_res = []
    print(st.session_state.claim)
    hits = search_fc(st.session_state.claim)
    process_table = pd.DataFrame(search_fc(st.session_state.claim), columns=["id", "article_url"])
    # process_table.set_index('id', inplace=True)
    
    process_table.insert(loc=0,column="verdict", value=None)

    stop = False

    my_bar = st.progress(0, text="test")

    for idx, h in enumerate(hits):

        my_bar.progress((idx + 1)/len(hits), str(idx) + "/" + str(len(hits)))

        if stop:
            st.session_state.annotated_res.append(sents)
            continue
            
    
        sents = sent_tokenize(h['contents'])

        seg_sents = [word_tokenize(s, format="text") for s in sents]

        claim = word_tokenize(st.session_state.claim, format="text")


        re = predict_fc(seg_sents, claim)

        rationale_ids = re["predicted_rationale"]
        if rationale_ids == []:
            rationale_ids = [re["rationale_probs"].argmax()]
        
        st.session_state.annotated_res.append([(s, re["predicted_label"]) if idx in rationale_ids else s for idx, s in enumerate(sents)])

        process_table.loc[idx, "verdict"] = re["predicted_label"]


        if re["predicted_label"] != "NEI" and not st.session_state.check_all:
            stop = True

    my_bar.empty()

    st.session_state.selection_table = process_table


col1, col2 = st.columns([4,6])

with col1:
    st.text_input(label="claim", key="claim", value=st.session_state.claim)
    st.button("get sample query", on_click=get_sample_query)
    st.toggle("check all", key="check_all")
    st.button("check", on_click=factcheck_button)

    if len(st.session_state.selection_table) > 0:
        selection = dataframe_with_selections(st.session_state.selection_table)
        st.session_state.fc_annotated_re = []
        for i in selection:
            st.session_state.fc_annotated_re.append("\n\n   " + str(i) + "\n\n   ")
            st.session_state.fc_annotated_re += st.session_state.annotated_res[i]


with col2:
    annotated_text(st.session_state.fc_annotated_re)



