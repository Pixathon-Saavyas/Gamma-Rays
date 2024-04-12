from uagents import Model, Agent, Bureau, Context


# models
class AiMessage(Model):
    msg: str


class UserMessage(Model):
    msg: str


def append_to_file(filename, value):
    """Appends a value to the given text file.

    Args:
        filename: The name of the text file.
        value: The value to be appended (can be any data type that can be converted to a string).
    """
    with open(filename, "a") as file:
        file.write(str(value) + "\n")  # Convert value to string and add newline


# file to which data is pushed
filename = "src/agents/msgs.txt"

ass_agent = Agent(
    "Assistant",
    seed="I am here to help",
    port=8001,
    endpoint=["http://127.0.0.1:8001/submit"],
)

USER_ADDRESS = "agent1q0qu50asf9dq5y7vpumtkv5d4g79rsw28cma5mg3v5r6qt8y2yr6x75zycm"


@ass_agent.on_event("startup")
async def startup(ctx: Context):
    # global conversation_history
    ctx.storage.set("filename", "src/agents/msgs.txt")

    initial_msg = "Hello, I am Leo. I'm here to listen to your concerns and help you in any way I can. Can you tell me a little bit about what's been troubling you? "
    ctx.logger.info(initial_msg)
    initial_msg_store = f"Assessment Agent : {initial_msg}"
    filename = ctx.storage.get("filename")
    append_to_file(filename=filename, value=initial_msg_store)
    await ctx.send(USER_ADDRESS, AiMessage(msg=initial_msg))


@ass_agent.on_message(model=UserMessage)
async def handle_user_message(ctx: Context, sender: str, message: UserMessage):
    filename = ctx.storage.get("filename")
    response = "Thank you for sharing"
    ctx.logger.info(response)
    # append data to file
    append_to_file(filename=filename, value=f"Assessment Agent : {response}")
    await ctx.send(USER_ADDRESS, AiMessage(msg=response))


if __name__ == "__main__":
    ass_agent.run()
