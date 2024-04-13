from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import LLMChain
from transformers import AutoTokenizer, AutoModelWithLMHead
import warnings, json, re


warnings.filterwarnings(
    "ignore", category=FutureWarning
)  # To suppress the first warning
warnings.filterwarnings("ignore", category=UserWarning)
tokenizer = AutoTokenizer.from_pretrained(
    "mrm8488/t5-base-finetuned-emotion", use_fast=False, legacy=False
)

model = AutoModelWithLMHead.from_pretrained("mrm8488/t5-base-finetuned-emotion")


def get_emotion(text):
    input_ids = tokenizer.encode(text + "</s>", return_tensors="pt")

    output = model.generate(input_ids=input_ids, max_length=2)

    dec = [tokenizer.decode(ids) for ids in output]
    label = dec[0]
    label = re.sub(r"<pad>", "", label)
    # return label
    return label


llm = ChatGoogleGenerativeAI(
    model="gemini-pro", google_api_key="AIzaSyA0SThtOf3QoNJLr12CiDwkiTtUafL1rXE"
)



def append_to_file(filename, value):
    with open(filename, "a") as file:
        file.write(str(value) + "\n")  # Convert value to string and add newline


def read_file_as_string(filename):
    with open(filename, "r") as file:
        return file.read()


def generate_gpt_response(user_message, filename):
    user_message = user_message
    filename = filename
    conversation_history = read_file_as_string(filename=filename)

    conv_prompt = PromptTemplate.from_template(
        """You are an expert mental therapist./
        Your task is to confront the user for his problems and ask critical questions to understand his mental health. You have to somehow ask the user about his symptoms, possible causes(relationship issues, health issues, sad demise) and carry on the conversation. The following is the conversation so far, continue asking questions. \
        Speak with the user in a very assistive and helpful manner.

    **Conversation History:**

    {conversation_history}

    **User Input:**

    {user_input}

    **Respond:**"""
    )

    conv_chain = LLMChain(llm=llm, prompt=conv_prompt, verbose=False)
    # conversation_history=""
    response = conv_chain.run(
        conversation_history=conversation_history, user_input=user_message
    )
    return response


def generate_final_report(data):
    # filename=filename
    data = data
    # conversation_history=read_file_as_string(filename=filename)
    conv_prompt = PromptTemplate.from_template(
        """You are an expert mental therapist./
    We are providing you with the a conversational data between between a user and a assessment chatbot. /
    Based on the conversation history provided, you have to output a final assessment of the user. We have also tagged all the user sentences with emotions detection deep learning model, please consider the emotions while generating the response./
    Return the response only as a json object starting and ending with curly brackets with the following keys and value-/ condition_of_patient : basic/mediocre/severe/, possible_causes : [list of possible causes discussed],/
    
                                               
    **Conversation History:**

    {conversation_history}

    **Respond:** """
    )

    conv_chain = LLMChain(llm=llm, prompt=conv_prompt, verbose=False)
    # conversation_history=""
    response = conv_chain.run(conversation_history=data)
    return response

