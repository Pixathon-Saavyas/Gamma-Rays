from transformers import AutoTokenizer, AutoModelWithLMHead
import warnings
import re
warnings.filterwarnings("ignore", category=FutureWarning)  # To suppress the first warning
warnings.filterwarnings("ignore", category=UserWarning)
tokenizer = AutoTokenizer.from_pretrained("mrm8488/t5-base-finetuned-emotion",use_fast=False,legacy=False)

model = AutoModelWithLMHead.from_pretrained("mrm8488/t5-base-finetuned-emotion")

def get_emotion(text):
  input_ids = tokenizer.encode(text + '</s>', return_tensors='pt')

  output = model.generate(input_ids=input_ids,
               max_length=2)

  dec = [tokenizer.decode(ids) for ids in output]
  label = dec[0]
  label=re.sub(r"<pad>", "", label)
  # return label
  return label

resp=get_emotion("i feel as if i havent blogged in ages are at least truly blogged i am doing an update cute")# Output: 'joy'

print(resp)