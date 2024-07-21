from interactions import Color, Embed, Extension, listen, Client, Member


class GreetExtension(Extension):
    def __init__(self, bot: Client):
        self.bot: Client = bot
        self.greetchannel: int = 1264470315078258723

    @listen()
    async def on_member_add(self, event):
        member: Member = event.member
        embed: Embed = Embed(
            title="**welcome to sage's haven!**",
            description=f"<@{member.id}>, enjoy your stay!",
            color=Color.from_rgb(83, 37, 115)
        )
        thumbnail_url: str = "https://cdn.discordapp.com/attachments/1261830193669083277/1264575885277925438/IMG_1129.png"
        embed.set_image(url=thumbnail_url)
        embed.set_footer(
            text=(
                "it would be lovely if you showed proof of payment so I "
                "don't waste my time, if not thats okay too! (ps payment "
                "proof doesn't mean I go first!)"
            )
        )
        author_url: str = "https://cdn.discordapp.com/attachments/1261830193669083277/1264380724752941086/IMG_1104.png"
        embed.set_author(name="Sage's Haven", icon_url=author_url)
        channel = await self.bot.fetch_channel(self.greetchannel)
        await channel.send(f"||<@{member.id}>||", embed=embed)
