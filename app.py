from interactions import Client
from utils import logutils
import interactions
import os


logger = logutils.CustomLogger(__name__)
client = Client(
    token="YOUR_BOT_TOKEN",
    intents=interactions.Intents.ALL,
)


@client.listen()
async def on_ready():
    logger.info(f"We have logged in as {client.app.name}")
    logger.info(f"User ID: {client.app.id}")
    logger.info(f"Connected to {len(client.guilds)} guilds")


if __name__ == "__main__":
    extensions = [
        f"extensions.{f[:-3]}"
        for f in os.listdir("extensions")
        if f.endswith(".py") and not f.startswith("_")
    ]
    for ext in extensions:
        try:
            client.load_extension(ext)
            logger.info(f"Loaded extension {ext}")
        except interactions.errors.ExtensionLoadException as exc:
            logger.error(
                f"Failed to load extension {ext}: {exc}",
                exc_info=exc
            )
    client.start()
