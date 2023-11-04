#星等評論model
from transformers import TextClassificationPipeline
from transformers import AutoModelForSequenceClassification, TrainingArguments, Trainer
from transformers import BertTokenizer, BertModel, BertConfig, BertTokenizerFast

def ratemodel(comment):
    max_seq_length = 512
    tokenizer = BertTokenizerFast.from_pretrained('bert-base-chinese',max_length=max_seq_length,padding='max_length', truncation=True)
    ##路徑記得更換 只能用絕對路徑
    new_model = AutoModelForSequenceClassification.from_pretrained("C:/Users/Blue/Desktop/資策會大數據/網站/Flask_travel_1.8.7/model/check",output_attentions=True)
    PipelineInterface = TextClassificationPipeline(model=new_model, tokenizer=tokenizer, return_all_scores=False)
    result = PipelineInterface(str(comment))
    return result

# print(ratemodel("好玩"))

