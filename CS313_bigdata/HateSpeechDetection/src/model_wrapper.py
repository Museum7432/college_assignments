from .data import WORKSPACE, collate_fn_factory
from .model import phoBert_CNN
from transformers import AutoModel, AutoTokenizer
from torch.nn import functional as F
import numpy as np
import torch


class model_wrapper:
    def __init__(self, checkpoint_path=None, device="cuda"):
        self.workspace = WORKSPACE()

        if checkpoint_path is None:
            checkpoint_path = self.workspace.files_path["phobertCNN.ckpt"]

        model = phoBert_CNN.load_from_checkpoint(
            checkpoint_path=checkpoint_path, map_location=device
        )

        model.eval()
        model.freeze()
        self.model = model

        self.tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base-v2")

        self.collate_fn = collate_fn_factory()

        self.id2label = np.array(["clean", "offensive", "hate speech"])

        self.device = device

    def to_device(self, batch):
        for k in batch.keys():
            batch[k] = batch[k].to(self.device)
        return batch

    def format_result(self, probs):
        label = np.argmax(probs)
        label = self.id2label[label]

        probs = probs.tolist()

        return {"verdict": label, "probs": probs, "labels": self.id2label.tolist()}

    def predict(self, texts):
        texts = self.workspace.preprocess_text(texts)

        batch = [self.tokenizer(t) for t in texts]

        batch = self.collate_fn(batch)

        batch = self.to_device(batch)

        logits = self.model(
            input_ids=batch["input_ids"],
            attention_mask=batch["attention_mask"],
        )

        probs = F.softmax(logits, dim=-1)

        probs = probs.cpu().numpy()

        return [self.format_result(re) for re in probs]
