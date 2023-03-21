from kspi.command.context import CommandContext
from kspi.command.language import provider



@provider
def launch_pad(ctx: CommandContext=None):
    return ctx.ksp.space_center.launch_pad