import os
# from dotenv import load_dotenv
# import langchain as langchain
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import LLMChain


# load_dotenv()

# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key="AIzaSyA0SThtOf3QoNJLr12CiDwkiTtUafL1rXE")

conv_prompt = PromptTemplate.from_template("""You are an expert mental therapist./
        Your task is to confront the user for his problems and ask critical questions to understand his mental health. You have to somehow ask the user about his symptoms, possible causes(relationship issues, health issues, sad demise) and carry on the conversation. The following is the conversation so far, continue asking questions. \
        Speak with the user in a very assistive and helpful manner.

    **Conversation History:**

    {conversation_history}

    **User Input:**

    {user_input}

    **Respond:**""")

conv_chain = LLMChain(llm=llm, prompt=conv_prompt, verbose=True)
conversation_history=""

count=0
while count!=10:
  
  user_input=input()
  
  response=conv_chain.run(conversation_history="",user_input=user_input)
  print(response)
  conversation_history= f"{conversation_history} \n\n user input : {user_input} response : {response} \n\n\n"
  count=count+1
