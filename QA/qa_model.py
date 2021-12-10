import time
import logging
import re
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import T5ForConditionalGeneration, T5Tokenizer, AdamW
import pytorch_lightning as pl

tokenizer = T5Tokenizer.from_pretrained('t5-base')

class QADataset(Dataset):
    def __init__(
            self,
            data, #:pd.DataFrame
            source_max_token_len: int = 396,
            target_max_token_len: int = 32,
        ):
        self.data =  data
        self.source_max_token_len =  source_max_token_len
        self.target_max_token_len =  target_max_token_len
        self.tokenizer = tokenizer
    
    def __len__(self):
        return len(self.data)

    def __getitem__(self, index: int):
        data_row = self.data.iloc[index]
        source_encoding = self.tokenizer(
            data_row['question'],
            data_row['context'],
            max_length=self.source_max_token_len,
            padding='max_length',
            truncation="only_second",
            return_attention_mask=True,
            add_special_tokens=True,
            return_tensors="pt"
            )
        target_encoding = self.tokenizer(
            data_row['answer_text'],
            max_length=self.target_max_token_len,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            add_special_tokens=True,
            return_tensors="pt"
            )
        labels = target_encoding['input_ids']
        labels[labels==0] = -100
        return dict(
            question=data_row['question'],
            context=data_row['context'],
            answer_text=data_row['answer_text'],
            input_ids=source_encoding["input_ids"].flatten(),
            attention_mask=source_encoding['attention_mask'].flatten(),
            labels=labels.flatten()
        )

class DataModule(pl.LightningDataModule):
    
    def __init__(
            self,
            train_df,
            test_df,
            batch_size: int = 8,
            source_max_token_len: int = 396,
            target_max_token_len: int = 32,
        ):
        super().__init__()
        self.train_df = train_df
        self.test_df = test_df
        self.batch_size = batch_size
        self.source_max_token_len = source_max_token_len
        self.target_max_token_len = target_max_token_len

    def setup(self):
        self.train_dataset = QADataset(
            self.train_df,
            self.source_max_token_len,
            self.target_max_token_len
        )
        self.test_dataset = QADataset(
            self.test_df,
            self.source_max_token_len,
            self.target_max_token_len
        )

    def train_dataloader(self):
        return DataLoader(
            self.train_dataset,
            batch_size=self.batch_size,
            shuffle=True,
            num_workers=4
        )

    def val_dataloader(self):
        return DataLoader(
            self.test_dataset,
            batch_size=self.batch_size,
            num_workers=4
        )

    def test_dataloader(self):
        return DataLoader(
            self.test_dataset,
            batch_size=1,
            num_workers=4
        )

class QAModel(pl.LightningModule):

    def __init__(self):
        super().__init__()
        self.model = T5ForConditionalGeneration.from_pretrained('t5-base', return_dict=True)

    def forward(self, input_ids, attention_mask, labels=None):
        output = self.model(
            input_ids, 
            attention_mask=attention_mask,
            labels=labels)
        return output.loss, output.logits

    def training_step(self, batch, batch_idx):
        input_ids = batch['input_ids']
        attention_mask=batch['attention_mask']
        labels = batch['labels']
        loss, outputs = self(input_ids, attention_mask, labels)
        self.log("train_loss", loss, prog_bar=True, logger=True)
        return {
            "loss": loss, 
            "predictions":outputs, 
            "labels": labels
        }

    def validation_step(self, batch, batch_idx):
        input_ids = batch['input_ids']
        attention_mask=batch['attention_mask']
        labels = batch['labels']
        loss, outputs = self(input_ids, attention_mask, labels)
        self.log("val_loss", loss, prog_bar=True, logger=True)
        return loss

    def test_step(self, batch, batch_idx):
        input_ids = batch['input_ids']
        attention_mask=batch['attention_mask']
        labels = batch['labels']
        loss, outputs = self(input_ids, attention_mask, labels)
        self.log("test_loss", loss, prog_bar=True, logger=True)
        return loss

    def configure_optimizers(self):
        optimizer = AdamW(self.parameters(), lr=0.0001)
        return optimizer

def generate_answer(question, trained_model):
    source_encoding = tokenizer(
        question["question"],
        question['context'],
        max_length = 396,
        padding="max_length",
        truncation="only_second",
        return_attention_mask=True,
        add_special_tokens=True,
        return_tensors="pt"
    )
    generated_ids = trained_model.model.generate(
        input_ids=source_encoding["input_ids"],
        attention_mask=source_encoding["attention_mask"],
        num_beams=1,  # greedy search
        max_length=80,
        repetition_penalty=2.5,
        early_stopping=True,
        use_cache=True)
    preds = [
            tokenizer.decode(generated_id, skip_special_tokens=True, clean_up_tokenization_spaces=True)
            for generated_id in generated_ids
    ]
    return "".join(preds)