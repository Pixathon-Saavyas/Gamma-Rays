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


# File to which converstation data is appended
filename = "src/agents/msgs.txt"

user_agent = Agent(
    "User",
    seed="I am a stressed user",
    port=8000,
    endpoint=["http://127.0.0.1:8000/submit"],
)

ASSESSMENT_AGENT = "agent1qgc6atqzr2n6mcn6uqr96fm678qltm6wrnjpzxn890x85q4ky304ghdz3yy"


@user_agent.on_message(model=AiMessage)
async def handle_message(ctx: Context, sender: str, message: AiMessage):
    # take user input
    if ctx.storage.has("filename"):
        filename = ctx.storage.get("filename")
    else:
        filename = "src/agents/msgs.txt"
        ctx.storage.set("filename", "src/agents/msgs.txt")

    user_input = input("User: ")
    user_msg_store = f" User : {user_input}"
    # append user message to file
    print(filename)
    append_to_file(filename=filename, value=user_msg_store)
    print("appended to txt file")

    await ctx.send(ASSESSMENT_AGENT, UserMessage(msg=user_input))


if __name__ == "__main__":
    user_agent.run()
