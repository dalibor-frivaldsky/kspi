from kspi.command.context import CommandContext
from kspi.command.language import operation
from kspi.ksp.system import LaunchSite



@operation
def ship_from_spacecenter(craft_directory: str, craft_name: str, launch_site: LaunchSite, name: str, ctx: CommandContext = None):
    ctx.ksp.space_center.launch_ship(craft_directory, craft_name, launch_site)
    vessel = ctx.ksp.scene.active_vessel
    vessel.name = name