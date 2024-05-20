import streamlit as st

from src.streamlit_helper import get_args,get_predict_fc
import plotly.express as px



st.set_page_config(
    page_title="phobertCNN Demo",
    # layout="wide"
)

args = get_args()

# st.write(args)



predict_fc = get_predict_fc(
    checkpoint_path = args["checkpoint_path"], 
    device=args["device"], 
    batch_size=args["batch_size"]
)



def check():
    text = st.session_state.text

    result = predict_fc([text])[0]

    fig = px.pie(values=result["probs"], names=result["labels"],title=f"The entered text is {result['verdict']}")

    fig.update_traces(textposition='inside', textinfo='value+label')
    st.plotly_chart(fig, use_container_width=True)

st.text_input(label="text", key="text")
st.button("check", on_click=check)


plot_spot = st.container()