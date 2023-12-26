import torch

data = torch.load("checkpoints/fever_sci.ckpt", map_location="cpu")

keys = list(data["state_dict"].keys())

for k in keys:
    if k.startswith(("rationale_classifier", "label_classifier")):
        print(k)
        del data["state_dict"][k]

torch.save(data, "checkpoints/fever_sci_mod.ckpt")