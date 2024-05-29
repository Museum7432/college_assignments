from .model_wrapper import model_wrapper
from service_streamer import ThreadedStreamer
import streamlit as st
import argparse
import torch


@st.cache_resource
def get_predict_fc(checkpoint_path, device, batch_size, mtype="phoBert_CNN"):
    model = model_wrapper(
        checkpoint_path=checkpoint_path,
        device=device,
        mtype=mtype
    )

    streamer = ThreadedStreamer(model.predict, batch_size=batch_size, max_latency=0.1)

    @st.cache_data
    def predict_fc(texts):
        outputs = streamer.predict(texts)

        return outputs
        
    return predict_fc



@st.cache_data
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cuda", action='store_true', help="use cuda if available")
    parser.add_argument("--checkpoint_path", type=str,help="path to model checkpoint", default=None)
    parser.add_argument("--batch_size", type=int,default=1)
    args = parser.parse_args()

    args = vars(args)

    args["device"] = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    if args["cuda"]:
        args["device"] = "cuda"

    return args
