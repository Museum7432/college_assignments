import gdown
import os
import numpy as np
import pandas as pd
import re
from torch.utils.data import DataLoader, Dataset, random_split
import emoji
from transformers import AutoModel, AutoTokenizer
import torch
import py_vncorenlp


class _Dataset(Dataset):
    def __init__(self, texts, labels):
        self.texts = texts
        self.labels = labels

        self.tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base-v2")

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):

        text = self.texts[idx]

        tokenized = self.tokenizer(text)

        item = {
            "input_ids": tokenized["input_ids"],
            "attention_mask": tokenized["attention_mask"],
        }

        if self.labels is None:
            return item

        item["label"] = self.labels[idx]

        return item


def collate_fn_factory():
    fields_to_pad = ["input_ids", "attention_mask"]

    pad_values = [1, 0]

    def _pad(arrs, constant_values=0, pad_width_fn=lambda l: ((0, l))):
        target_length = max([len(i) for i in arrs])

        # the sequence length must be larger than the kernel size
        target_length = max(target_length, 6)

        return np.array(
            [
                np.pad(
                    i,
                    pad_width_fn(target_length - len(i)),
                    "constant",
                    constant_values=constant_values,
                )
                for i in arrs
            ]
        )

    def collate_fn(items):
        batch = {}

        for f in items[0].keys():
            batch[f] = [i[f] for i in items]

        for f, v in zip(fields_to_pad, pad_values):
            batch[f] = _pad(batch[f], constant_values=v)

        for f in batch.keys():
            batch[f] = torch.tensor(batch[f])
        return batch

    return collate_fn

def loaddicchar():
    dic = {}
    char1252 = 'à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ'.split(
        '|')
    charutf8 = "à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ".split(
        '|')
    for i in range(len(char1252)):
        dic[char1252[i]] = charutf8[i]
    return dic

# coding=utf-8
# Copyright (c) 2021 VinAI Research

dict_map = {
    "òa": "oà",
    "Òa": "Oà",
    "ÒA": "OÀ",
    "óa": "oá",
    "Óa": "Oá",
    "ÓA": "OÁ",
    "ỏa": "oả",
    "Ỏa": "Oả",
    "ỎA": "OẢ",
    "õa": "oã",
    "Õa": "Oã",
    "ÕA": "OÃ",
    "ọa": "oạ",
    "Ọa": "Oạ",
    "ỌA": "OẠ",
    "òe": "oè",
    "Òe": "Oè",
    "ÒE": "OÈ",
    "óe": "oé",
    "Óe": "Oé",
    "ÓE": "OÉ",
    "ỏe": "oẻ",
    "Ỏe": "Oẻ",
    "ỎE": "OẺ",
    "õe": "oẽ",
    "Õe": "Oẽ",
    "ÕE": "OẼ",
    "ọe": "oẹ",
    "Ọe": "Oẹ",
    "ỌE": "OẸ",
    "ùy": "uỳ",
    "Ùy": "Uỳ",
    "ÙY": "UỲ",
    "úy": "uý",
    "Úy": "Uý",
    "ÚY": "UÝ",
    "ủy": "uỷ",
    "Ủy": "Uỷ",
    "ỦY": "UỶ",
    "ũy": "uỹ",
    "Ũy": "Uỹ",
    "ŨY": "UỸ",
    "ụy": "uỵ",
    "Ụy": "Uỵ",
    "ỤY": "UỴ",
    }

def VietnameseToneNormalization(text):
    for i, j in dict_map.items():
        text = text.replace(i, j)
    return text

class WORKSPACE:
    def __init__(self, dataset_dir=None):
        # download data to the dataset folder
        if dataset_dir is None:
            dataset_dir = "./dataset"

        os.makedirs(dataset_dir, exist_ok=True)

        files = [
            ["test-HSD.csv", "1Oj-h-qDhCdq_9GnSPLFjbvbwNTykUXG9"],
            ["train-HSD.csv", "1r3igHyD9jgl--zLbTcO-Gu_uC6em5U0b"],
            ["val-HSD.csv", "1Gdj6Q_aq468LGpHDrv2ORO4gaKumEVXi"],
            ["vietnamese-stopwords-dash.txt", "1CAWxF85YgT-S3N9_1AnLGgSbXaBjls7G"],
            ["vietnamese_stopwords.txt", "1wyQh4amy87iT4Wiuer8_S4t27geboEpD"],
            ["teencode.txt", "1ucJiBxFQqksMVFhguIGrE26yeDg5CSXc"],
            ["phobertCNN.ckpt", "1hKfQrl0vrEo3kKVsCHCHQeKRfWPfqniD"]
        ]

        self.files_path = {}

        for file_name, fid in files:
            output_path = os.path.join(dataset_dir, file_name)
            self.files_path[file_name] = output_path

            if os.path.isfile(output_path):
                continue
            gdown.download(id=fid, output=output_path)

        self.load_()

        cwd = os.getcwd()
        vncorenlp_path = os.path.abspath(os.path.join(dataset_dir, "vncorenlp"))
        os.makedirs(vncorenlp_path, exist_ok=True)
        py_vncorenlp.download_model(save_dir=vncorenlp_path)

        self.vncorenlp = py_vncorenlp.VnCoreNLP(
            annotators=["wseg"], save_dir=vncorenlp_path
        )

        os.chdir(cwd)
        print(os.getcwd())

    def load_(self):
        # for un-segmented text
        self.stopwords = []
        with open(self.files_path["vietnamese_stopwords.txt"]) as f:
            for line in f:
                dd = line.strip("\n")
                self.stopwords.append(dd)
        self.stopwords = set(self.stopwords)

        # for word-segmented text
        self.WS_stopwords = []
        with open(self.files_path["vietnamese_stopwords.txt"]) as f:
            for line in f:
                dd = line.strip("\n")
                self.WS_stopwords.append(dd)
        self.WS_stopwords = set(self.WS_stopwords)

        self.teencode = []
        with open(self.files_path["teencode.txt"]) as f:
            for line in f:
                dd = line.strip("\n")
                self.teencode.append(dd)
        self.teencode = set(self.teencode)

        self.dicchar = loaddicchar()

    def remove_stop_words(self, texts, word_segmented=True):
        stop_words = self.WS_stopwords if word_segmented else self.stopwords
        texts = [
            " ".join([word for word in s.split() if word not in stop_words])
            for s in texts
        ]

        return texts

    @staticmethod
    def remove_emojy(texts):
        return [emoji.replace_emoji(s, replace="") for s in texts]

    def word_segmentation(self, texts):
        return [" ".join(self.vncorenlp.word_segment(s)) for s in texts]

    @staticmethod
    def remove_html(text):
        return re.sub(r"http\S+", "", text)

    def convert_unicode(self, txt):
        return re.sub(
            r'à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ',
            lambda x: self.dicchar[x.group()], txt)
    
    

    def preprocess_text(
        self,
        texts,
        word_segmentation=True,
        word_segmented_stop_word=True,
        remove_stop_words=True,
        lowercased=True,
    ):
        texts = self.remove_emojy(texts)

        # xóa khoảng trắng thừa
        texts = [" ".join(s.split()) for s in texts]

        texts = [self.remove_html(s) for s in texts]
        texts = [self.convert_unicode(s) for s in texts]

        texts = [VietnameseToneNormalization(s) for s in texts]

        if lowercased:
            texts = [s.lower() for s in texts]
        
        if word_segmentation:
            texts = self.word_segmentation(texts)

        if remove_stop_words:
            texts = self.remove_stop_words(
                texts, word_segmented=word_segmented_stop_word
            )

        return texts

    def _load_file(self, file_path, has_label=True, **preprocess_args):
        data = pd.read_csv(file_path)

        texts = data["Comment"]
        labels = data["Label"].values if has_label else None

        texts = [str(p) for p in list(texts)]

        texts = self.preprocess_text(texts=texts, **preprocess_args)

        return texts, labels

    def load_data(self, stage, **preprocess_args):
        has_labels = {"train": True, "val": True, "test": True}
        file_names = {
            "train": "train-HSD.csv",
            "val": "val-HSD.csv",
            "test": "test-HSD.csv",
        }

        assert stage in file_names.keys()

        fn = self.files_path[file_names[stage]]

        hl = has_labels[stage]

        tmp_texts, tmp_labels = self._load_file(
            file_path=fn,
            has_label=hl,
            word_segmentation=False, # the dataset have already been word segmented
            word_segmented_stop_word=True,
            **preprocess_args
        )
        texts, labels = [], []

        for i in range(len(tmp_texts)):
            if tmp_texts[i] is None or len(tmp_texts[i]) == 0:
                continue
            texts.append(tmp_texts[i])
            if hl:
                labels.append(tmp_labels[i])

        return texts, labels

    def get_dataloader(self, stage, batch_size=4, shuffle=True, num_workers=4):
        texts, labels = self.load_data(stage)

        dataset = _Dataset(texts, labels)

        return DataLoader(
            dataset,
            batch_size=batch_size,
            collate_fn=collate_fn_factory(),
            shuffle=shuffle,
            num_workers=num_workers,
        )
