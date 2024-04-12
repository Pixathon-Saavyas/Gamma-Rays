from uagents import Agent, Context, Bureau, Model

class Message(Model):
    message: str


alice = Agent(name="Alice", seed="alice recovery phase")
bob = Agent(name="Bob", seed="bob recovery phase")


@alice.on_interval(period=3.0)
async def send_message(ctx: Context):
    await ctx.send(bob.address, Message(message="Hello Bob"))


@alice.on_message(period=2.0)
async def alice_message_handler(ctx: Context, sender:str, message:Message):
    await ctx.logger.info(f"Alice Recived from {sender}: {message}")


@bob.on_message(period=2.0)
async def bob_message_handler(ctx: Context, sender:str, message:Message):
    ctx.logger.info(f"Bob Recived from {sender}: {message}")
    await ctx.send(alice.address, Message(message="Hello from Bob"))

bureau = Bureau()
bureau.add(alice)
bureau.add(bob)

if __name__ == "__main__":
    bureau.run()
