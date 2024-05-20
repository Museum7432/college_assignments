import lightning as L
from torch import nn
import transformers
from torch.nn import functional as F

import torch
from transformers import AutoModel
import torchmetrics

from transformers.optimization import get_linear_schedule_with_warmup

class phoBert_CNN(L.LightningModule):
    def __init__(self, output_dim=3, lr = 5e-5):
        super().__init__()
        self.lr = lr
        self.phobert = AutoModel.from_pretrained("vinai/phobert-base-v2")

        embedding_dim = self.phobert.embeddings.word_embeddings.embedding_dim

        region_sizes = [1, 2, 3, 5]
        n_filters = 32

        self.fc_input = nn.Linear(embedding_dim, embedding_dim)

        convs = []
        for s in region_sizes:
            convs.append(
                nn.Conv1d(
                    in_channels=embedding_dim,
                    out_channels=n_filters,
                    kernel_size=s,
                )
            )
        self.convs = nn.ModuleList(convs)

        self.fc = nn.Linear(len(region_sizes) * n_filters, output_dim)

        self.dropout = nn.Dropout(0.1)

        self.valid_f1 = torchmetrics.classification.F1Score(
            task="multiclass", num_classes=output_dim
        )
    
    def forward(self, input_ids, attention_mask=None):
        # batch_size, seq_len, embedding_size
        encoded = self.phobert(
            input_ids=input_ids, attention_mask=attention_mask
        ).last_hidden_state

        encoded = F.relu(self.fc_input(encoded))

        # batch_size, embedding_size, seq_len
        encoded = encoded.permute(0, 2, 1)

        convoluted = []
        for conv in self.convs:
            # batch_size, 32, seq_len - kernel_size + 1
            c = F.relu(conv(encoded))

            # extract sentence level representation
            # batch_size, 32
            c = c.max(-1).values

            convoluted.append(c)
        
        # batch_size, 32 * len(self.convs)
        convoluted = self.dropout(torch.hstack(convoluted))

        # batch_size, 3
        logits =  self.fc(convoluted)

        return logits

    def calc_loss(self, logits, label):

        logits = F.log_softmax(logits, dim=1)

        loss = F.nll_loss(logits, label, reduction="mean")

        return loss

    def training_step(self, batch):
        logits = self(
            input_ids=batch["input_ids"],
            attention_mask=batch["attention_mask"],
        )
        loss = self.calc_loss(logits, batch["label"])

        self.log("train_loss", loss.detach(), prog_bar=True)

        return loss
    

    def validation_step(self, batch):
        logits = self(
            input_ids=batch["input_ids"],
            attention_mask=batch["attention_mask"],
        )
        loss = self.calc_loss(logits, batch["label"])

        pred = logits.argmax(dim=1)

        self.valid_f1(pred.detach(), batch["label"])

        self.log("valid_f1", self.valid_f1, prog_bar=True)
        self.log("valid_loss", loss.detach(), prog_bar=True)

        return loss

    def num_steps(self) -> int:
        """Get number of steps"""
        # Accessing _data_source is flaky and might break
        dataset = self.trainer.fit_loop._data_source.dataloader()
        dataset_size = len(dataset)
        num_devices = max(1, self.trainer.num_devices)
        num_steps = (
            dataset_size
            * self.trainer.max_epochs
            // (self.trainer.accumulate_grad_batches * num_devices)
        )
        return num_steps

    def configure_optimizers(self):
        self.optimizer = torch.optim.AdamW(self.parameters(), lr=self.lr)

        # return self.optimizer
        num_steps = self.num_steps()
        
        self.lr_scheduler = get_linear_schedule_with_warmup(
            self.optimizer,
            num_warmup_steps=num_steps * 0.20,
            num_training_steps=num_steps,
        )

        return [self.optimizer], [{"scheduler": self.lr_scheduler, "interval": "step"}]
