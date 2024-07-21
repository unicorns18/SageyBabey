from interactions import (
    Extension, Client, Embed, Button, ButtonStyle, ComponentContext,
    Guild, Member, component_callback, slash_command
)


class RolesExtension(Extension):
    def __init__(self, bot: Client):
        self.bot: Client = bot
        self.roles_channel_id: int = 1264470387006373918
        self.age_roles = {
            "18+": 1264486999490953227,
            "13-17": 1264487040704053259
        }

    @slash_command(
        name="age_roles", description="Send age roles embed"
    )
    async def age_roles(self, ctx: ComponentContext):
        embed = Embed(
            title="Age Roles",
            description="Select your age role by clicking "
                        "the appropriate button."
        )
        buttons = [
            Button(
                style=ButtonStyle.PRIMARY,
                label=role_name,
                custom_id=f"role_button_{role_name.replace(' ', '_')}"
            )
            for role_name in self.age_roles.keys()
        ]
        channel = await self.bot.fetch_channel(self.roles_channel_id)
        await channel.send(embeds=embed, components=buttons)
        await ctx.send("Age roles embed sent!", ephemeral=True)

    @component_callback("role_button_18+")
    async def role_button_18_plus(self, ctx: ComponentContext):
        await self.handle_role_button(ctx, "18+")

    @component_callback("role_button_13-17")
    async def role_button_13_17(self, ctx: ComponentContext):
        await self.handle_role_button(ctx, "13-17")

    async def handle_role_button(self, ctx: ComponentContext, role_name: str):
        guild: Guild = await self.bot.fetch_guild(ctx.guild_id)
        member: Member = await guild.fetch_member(ctx.author_id)
        role_id = self.age_roles[role_name]

        if role_id not in [role.id for role in member.roles]:
            for r_name, r_id in self.age_roles.items():
                if r_id in [role.id for role in member.roles]:
                    role = guild.get_role(r_id)
                    await member.remove_role(role, reason="Age role change")
            role = guild.get_role(role_id)
            await member.add_role(role, reason="Age role change")
            message = f"{member.mention}, you have been assigned the " \
                      f"{role_name} role!"
            await ctx.send(message, ephemeral=True)
        else:
            await ctx.send("You already have this role!", ephemeral=True)
