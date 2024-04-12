from uagents import Model, Agent, Bureau, Context

# conversation_history=""

def append_to_file(filename, value):
  """Appends a value to the given text file.

  Args:
      filename: The name of the text file.
      value: The value to be appended (can be any data type that can be converted to a string).
  """
  with open(filename, "a") as file:
    file.write(str(value) + "\n")  # Convert value to string and add newline


# def generate_response(user_message):
   
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
    user_msg_store = f" User : {user_input}"
    #append user message to file
    print(filename)
    append_to_file(filename=filename, value=user_msg_store)
    print("appended to txt file")

    await ctx.send(ass_agent.address, user_message(msg=user_input))

@ass_agent.on_message(user_message)
async def handle_user_message(ctx: Context, sender:str, message: user_message):
    # user_message=message.msg
    filename=ctx.storage.get("filename")
    response="Thank you for sharing"


    ctx.logger.info(response)
    append_to_file(filename=filename, value=f"Assessment Agent : {response}")
    await ctx.send(user_agent.address, ai_message(msg=response))


b=Bureau()
b.add(user_agent)
b.add(ass_agent)

if __name__ == "__main__":
    b.run()