from uagents import Model, Agent, Bureau, Context
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import LLMChain
import json
from transformers import AutoTokenizer, AutoModelWithLMHead
import warnings
import re
import pandas as pd

warnings.filterwarnings(
    "ignore", category=FutureWarning
)  # To suppress the first warning
warnings.filterwarnings("ignore", category=UserWarning)
tokenizer = AutoTokenizer.from_pretrained(
    "mrm8488/t5-base-finetuned-emotion", use_fast=False, legacy=False
)


df = pd.read_csv("src/agents/data.csv")


def get_top_5_therapists(city):
    # Filter therapists based on the input city
    therapists_in_city = df[df["city"].str.lower() == city.lower()]

    if therapists_in_city.empty:
        print("No therapists found in the specified city.")
        return

    # Sort therapists based on years_of_exp in descending order and get the top 5
    top_5_therapists = therapists_in_city.sort_values(
        by="years_of_exp", ascending=False
    ).head(5)

    return top_5_therapists


llm = ChatGoogleGenerativeAI(
    model="gemini-pro", google_api_key="AIzaSyA0SThtOf3QoNJLr12CiDwkiTtUafL1rXE"
)


def generate_final_report(data):
    data = data
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
    response = conv_chain.run(conversation_history=data)
    return response


filename = "src/agents/msgs.txt"


class ai_message(Model):
    msg: str


therapy_agent = Agent(
    "Therapy",
    seed="I give therapy",
    port=8000,
    endpoint=["http://127.0.0.1:8000/submit"],
)


@therapy_agent.on_message(ai_message)
async def user_message_handler(ctx: Context, sender: str, message: ai_message):
    ctx.logger.info("generating final report")
    response = generate_final_report(message.msg)
    print(response)
    response = json.loads(response)
    ctx.logger.info(ctx.address)
    ctx.logger.info(response)
    if response["condition_of_patient"] == "severe":
        ctx.logger.info(
            "We have analysed your condition and we think that you should consult to a therapist. \n Please enter your city : "
        )
        city = input("City: ")
        therapists = get_top_5_therapists(city)
        ctx.logger.info(f"Here are top 5 therapists in {city} : \n {therapists}")

    else:
        ctx.logger.info(
            "We have analysed your condition and we think that you can get back into shape by doing this course : "
        )


if __name__ == "__main__":
    therapy_agent.run()
