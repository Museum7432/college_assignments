import streamlit as st

from src.streamlit_helper import get_args, get_predict_fc
import plotly.express as px


st.set_page_config(
    page_title="HSD Demo",
    # layout="wide"
)

args = get_args()


option = st.selectbox("model type:", ("phoBert_CNN", "phoBert"))


predict_fc = get_predict_fc(
    checkpoint_path=args["checkpoint_path"],
    device=args["device"],
    batch_size=args["batch_size"],
    mtype=option,
)


def check():
    text = st.session_state.text

    result = predict_fc([text])[0]

    fig = px.pie(
        values=result["probs"],
        names=result["labels"],
        title=f"The entered text is {result['verdict']}",
        color=result["labels"],
        color_discrete_map={
            "clean": "green",
            "offensive": "yellow",
            "hate speech": "red"
        },
    )

    fig.update_traces(textposition="inside", textinfo="value+label")
    st.plotly_chart(fig, use_container_width=True)


st.text_input(label="text", key="text")
st.button("check", on_click=check)


plot_spot = st.container()
