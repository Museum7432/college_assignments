import sys
sys.path.append("./src")

import streamlit as st
from annotated_text import annotated_text
from src.streamlit_helper import get_args, get_split_sents, get_predict_fc, get_search_fc

import pandas as pd

import random
import numpy as np

###############################################
# https://discuss.streamlit.io/t/problem-share-session-state-on-multipages/27755/8
# https://stackoverflow.com/questions/74968179/session-state-is-reset-in-streamlit-multipage-app
for k, v in st.session_state.to_dict().items():
    st.session_state[k] = v
###############################################

st.set_page_config(layout="wide")


args = get_args()

split_sents = get_split_sents()
predict_fc = get_predict_fc(
    checkpoint_path = args["checkpoint_path"], 
    device=args["device"], 
    batch_size=args["batch_size"]
)
search_fc = get_search_fc(index_dir=args["index_dir"])

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
        "Kareena Kapoor was a commercial failure.",
        "Natasha Lyonne was born in 1995.",
        "The Maze Runner is a sports competition.",
        "Designated Survivor (TV series) is a television show.",
        "Johnny Van Zant is incapable of being a musician.",
        "Sacre-Coeur, Paris is an embodiment of cultism.",
        "Pierce County, Washington is the home of a football team.",
        "Ricardo Montalbán was Mexican politician.",
        "Sabbir Khan directed a movie.",
        "The Office (US) was filmed in front of a live audience.",
        "Coins of the Swiss franc are used in Hungary.",
        "Richard Dawson died on June 2nd, 2012",
        "Hezbollah received accounting training from Iran.",
        "Live Nation Entertainment is a global energy company.",
        "Fred Seibert only has a career as a gospel record producer.",
        "The Guardian is a US daily newspaper",
        "The Guardian newspaper is biased",
        "Soviet shot down a Korean civilian aircraft in 1978",
        "Hanoi is the capital of japan",
        "HaNoi is the capital of Vietnam",
        "The Theatre Royal in Bath has a capacity of 800"
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
    process_table = pd.DataFrame(search_fc(st.session_state.claim), columns=["id", "title"])
    # process_table.set_index('id', inplace=True)
    
    process_table.insert(loc=0,column="verdict", value=None)

    stop = False

    my_bar = st.progress(0, text="test")

    for idx, h in enumerate(hits):

        my_bar.progress((idx + 1)/len(hits), str(idx) + "/" + str(len(hits)))

        if stop:
            st.session_state.annotated_res.append(sents)
            continue
            
        
        sents = split_sents(h['contents'])

        re = predict_fc(sents, st.session_state.claim)

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



