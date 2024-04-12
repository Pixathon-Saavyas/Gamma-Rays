from uagents import Model, Agent, Bureau, Context
# import os
# from dotenv import load_dotenv
# import langchain as langchain

from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import LLMChain



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


from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key="AIzaSyA0SThtOf3QoNJLr12CiDwkiTtUafL1rXE")
# conversation_history=""

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
 

def generate_response(user_message,filename):
    user_message=user_message
    filename=filename
    conversation_history = read_file_as_string(filename=filename)

    conv_prompt = PromptTemplate.from_template("""You are an expert mental therapist./
        Your task is to confront the user for his problems and ask critical questions to understand his mental health. You have to somehow ask the user about his symptoms, possible causes(relationship issues, health issues, sad demise) and carry on the conversation. The following is the conversation so far, continue asking questions. \
        Speak with the user in a very assistive and helpful manner.

    **Conversation History:**

    {conversation_history}

    **User Input:**

    {user_input}

    **Respond:**""")

    conv_chain = LLMChain(llm=llm, prompt=conv_prompt, verbose=False)
    # conversation_history=""
    response=conv_chain.run(conversation_history=conversation_history,user_input=user_message)
    return response

def generate_final_report(filename):
    filename=filename
    conversation_history=read_file_as_string(filename=filename)
    conv_prompt = PromptTemplate.from_template("""You are an expert mental therapist./
        Your task is to confront the user for his problems and ask critical questions to understand his mental health. You have to somehow ask the user about his symptoms, possible causes(relationship issues, health issues, sad demise) and carry on the conversation. The following is the conversation so far, continue asking questions. \
        Speak with the user in a very assistive and helpful manner.

                                               
    **Conversation History:**

    {conversation_history}

    **Respond:** """)

    conv_chain = LLMChain(llm=llm, prompt=conv_prompt, verbose=False)
    # conversation_history=""
    response=conv_chain.run(conversation_history=conversation_history)
    return response
  
# Example usage
filename = "src/agents/msgs.txt"
# value1 = "This is the first value"
# value2 = 42  # Integer value

# append_to_file(filename, "hello")
# append_to_file(filename, value2)

class user_message(Model):
    msg:str

class ai_message(Model):
    msg:str

ass_agent=Agent("Assistant",seed="I am here to help")
user_agent=Agent("User",seed="I am a stressed user")
therapy_agent=Agent("Therapy",seed="I give therapy")

@ass_agent.on_event("startup")
async def startup(ctx: Context):
    # global conversation_history
    ctx.storage.set("filename","src/agents/msgs.txt")

    initial_msg="Hello, I am Leo. I'm here to listen to your concerns and help you in any way I can. Can you tell me a little bit about what's been troubling you? "
    ctx.logger.info(initial_msg)

    initial_msg_store=f"Assessment Agent : {initial_msg}"

    filename=ctx.storage.get("filename")

    append_to_file(filename=filename,value=initial_msg_store)
    # conversation_history = initial_msg
    #store initial message in storage
    # ctx.storage.set("conversation_history",initial_msg)

    # print(ctx.storage.get("conversation_history"))
    await ctx.send(user_agent.address, ai_message(msg=initial_msg))
                   
@user_agent.on_message(ai_message)
async def handle_message(ctx: Context, sender:str, message: ai_message):
    #take user input
    if ctx.storage.has("filename"):
       filename=ctx.storage.get("filename")
    else:
       filename = "src/agents/msgs.txt"
       ctx.storage.set("filename",'src/agents/msgs.txt')
       
    
    user_input = input("User: ")
    if user_input=="bye":
       print("inside exit")
       await ctx.send(therapy_agent.address, user_message(msg=user_input))
    else :    
    
    
        emotion=get_emotion(user_input)
        user_msg_store = f" User : {user_input} -> [Emotion Detection : {emotion}]"
        
        #append user message to file
        # print(filename)
        append_to_file(filename=filename, value=user_msg_store)
        # print("appended to txt file")

        await ctx.send(ass_agent.address, user_message(msg=user_input))

@ass_agent.on_message(user_message)
async def handle_user_message(ctx: Context, sender:str, message: user_message):
    # user_message=message.msg
    filename=ctx.storage.get("filename")

    response=generate_response(user_message=message.msg,filename=filename)

    ctx.logger.info(response)
    append_to_file(filename=filename, value=f"Assessment Agent : {response}")
    await ctx.send(user_agent.address, ai_message(msg=response))

@therapy_agent.on_message(user_message)
async def user_message_handler(ctx: Context, sender:str, message: user_message):
    ctx.logger.info("generating final report")


b=Bureau()
b.add(user_agent)
b.add(ass_agent)
b.add(therapy_agent)

if __name__ == "__main__":
    b.run()