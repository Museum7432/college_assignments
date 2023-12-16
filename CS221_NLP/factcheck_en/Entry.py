import sys
sys.path.append("./src")
import streamlit as st



from src.streamlit_helper import get_args

###############################################
# https://discuss.streamlit.io/t/problem-share-session-state-on-multipages/27755/8
# https://stackoverflow.com/questions/74968179/session-state-is-reset-in-streamlit-multipage-app
for k, v in st.session_state.to_dict().items():
    st.session_state[k] = v
###############################################


st.set_page_config(
    page_title="Demo",
    layout="wide"
)

st.title("Main Page")
st.sidebar.success("Select a page above.")


args = get_args()

st.write(args)
