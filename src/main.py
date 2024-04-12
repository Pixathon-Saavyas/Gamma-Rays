# develop a meet scheduling agent using uagents librarry
from uagents import Agent, Bureau, Context, Model

user = Agent("Greeshma", seed="Greeshma knows konkani")


@user.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info("Hi, Its started")


if __name__ == "__main__":
    user.run()
