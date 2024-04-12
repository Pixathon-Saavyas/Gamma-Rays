from uagents import Model, Agent, Context
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import LLMChain
import json
import pandas as pd
from transformers import AutoTokenizer, AutoModelWithLMHead
import warnings
import re
from langchain_google_genai import ChatGoogleGenerativeAI

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
    """Appends a value to the given text file.

    Args:
        filename: The name of the text file.
        value: The value to be appended (can be any data type that can be converted to a string).
    """
    with open(filename, "a") as file:
        file.write(str(value) + "\n")  # Convert value to string and add newline


def read_file_as_string(filename):
    with open(filename, "r") as file:
        return file.read()


def generate_response(user_message, filename):
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
    response = conv_chain.run(
        conversation_history=conversation_history, user_input=user_message
    )
    return response


# Example file in which temporary chat is stored
filename = "src/agents/msgs.txt"


class user_message(Model):
    msg: str


class ai_message(Model):
    msg: str


ass_agent = Agent(
    "Assistant",
    seed="I am here to help",
    port=8001,
    endpoint=["http://127.0.0.1:8001/submit"],
)

THERAPY_AGENT_ADD = "agent1qvkvy5x6s0h56hqulq0nn0ucqsc8lrpkmkupthr0qjs4nfel2ufmsrz6mpg"


@ass_agent.on_event("startup")
async def startup(ctx: Context):
    # global conversation_history
    ctx.storage.set("filename", "src/agents/msgs.txt")
    # assessment agent msg
    initial_msg = "Hello, I am Leo. I'm here to listen to your concerns and help you in any way I can. Can you tell me a little bit about what's been troubling you? "
    ctx.logger.info(initial_msg)
    # take user input
    user_input = input("User : ")
    # derive user emotion using hugging face api
    emotion = get_emotion(user_input)
    user_msg_store = f" User : {user_input} ->[emotion prediction : {emotion}]"
    conversation = f"Assessment Agent: {initial_msg} \n\n User: {user_msg_store}"

    await ctx.send(THERAPY_AGENT_ADD, ai_message(msg=conversation))


if __name__ == "__main__":
    ass_agent.run()
