from interactions import Button, ButtonStyle, Color, ComponentContext, Embed, \
    Extension, Client, Guild, Member, component_callback, slash_command


class VerifyExtension(Extension):
    def __init__(self, bot: Client):
        self.bot: Client = bot
        self.log_verifications: bool = True
        self.verifychannel: int = 1264470357683863562
        self.verify_role_id: int = 1264480932736536636
        self.log_channel_id: int = 1264543627217080320

    @slash_command(
        name="verify",
        description="Send a verification embed",
    )
    async def verify(self, ctx: ComponentContext):
        embed = Embed(
            title="Verification",
            description="Click the button below to verify your account."
        )
        button = Button(
            style=ButtonStyle.SUCCESS,
            label="Verify",
            custom_id="verify_button"
        )
        channel = await self.bot.fetch_channel(self.verifychannel)
        await channel.send(embeds=embed, components=[button])
        await ctx.send("Verification embed sent!", ephemeral=True)

    @component_callback("verify_button")
    async def verify_button(self, ctx: ComponentContext):
        guild: Guild = await self.bot.fetch_guild(ctx.guild_id)
        member: Member = await guild.fetch_member(ctx.author_id)

        if self.verify_role_id not in [role.id for role in member.roles]:
            role = guild.get_role(self.verify_role_id)
            await member.add_role(role, reason="User verified")
            await ctx.send(f"{member.mention}, you have been "
                           "verified!", ephemeral=True)

            if self.log_verifications:
                log_channel = await self.bot.fetch_channel(self.log_channel_id)
                log_embed = Embed(
                    title="Verification Log",
                    color=Color.from_rgb(83, 37, 115)
                )
                log_embed.add_field(
                    name="User",
                    value=f"{member} ({member.id})"
                )
                log_embed.add_field(
                    name="Joined At",
                    value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S")
                )
                log_embed.add_field(
                    name="Created At",
                    value=member.created_at.strftime("%Y-%m-%d %H:%M:%S")
                )
                log_embed.set_thumbnail(url=member.avatar_url)
                await log_channel.send(embed=log_embed)
        else:
            await ctx.send("You are already verified!", ephemeral=True)
