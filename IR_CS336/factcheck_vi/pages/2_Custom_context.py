import sys
sys.path.append("./src")

import streamlit as st
from annotated_text import annotated_text
from src.streamlit_helper import get_args, get_predict_fc
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

if "context" not in st.session_state:
    st.session_state["context"] = ""

if "claim" not in st.session_state:
    st.session_state["claim"] = ""

if "cus_annotated_re" not in st.session_state:
    st.session_state["cus_annotated_re"] = []

def button_check_custom():
    sents = sent_tokenize(st.session_state.context)
    seg_sents = [word_tokenize(s, format="text") for s in sents]

    claim = word_tokenize(st.session_state.claim, format="text")

    re = predict_fc(sents, claim)

    rationale_ids = re["predicted_rationale"]
    if rationale_ids == []:
        rationale_ids = [re["rationale_probs"].argmax()]
    
    cus_annotated_re = []

    for idx, s in enumerate(sents):
        if idx in rationale_ids:
            cus_annotated_re.append((s, re["predicted_label"]))
        else:
            cus_annotated_re.append(s)

    st.session_state.cus_annotated_re = cus_annotated_re

col1, col2 = st.columns([4,6])



with col1:
    st.text_area(label="context", key="context",height=500, value=st.session_state.context)
    st.text_input(label="claim", key="claim", value=st.session_state.claim)

    st.button("check", on_click=button_check_custom)

with col2:
    annotated_text(st.session_state.cus_annotated_re)