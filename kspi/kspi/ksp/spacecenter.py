from kspi.ksp.system import LaunchSite
from kspi.rpc.client import Connection



class SpaceCenter:

    def __init__(self, conn: Connection):
        self._conn = conn


    def launch_ship(self, craft_directory: str, craft_name: str, launch_site: LaunchSite):
        def perform(ctx):
            path_to_craft_file = ctx.clr.KSPUtil.ApplicationRootPath + "saves/" + ctx.clr.HighLogic.SaveFolder + "/Ships/" + craft_directory + "/" + craft_name + ".craft"
            ship_template = ctx.clr.ShipConstruction.LoadTemplate(path_to_craft_file)
            if ship_template is None:
                raise ValueError(f'The craft specified does not exist: {path_to_craft_file}')
            crew_manifest = ctx.clr.HighLogic.CurrentGame.CrewRoster.DefaultCrewForVessel(ship_template.config, previous=None, autohire=False)
            ctx.clr.FlightDriver.StartWithNewLaunch(
                path_to_craft_file,
                '', # missionFlagURL
                launch_site.name,
                crew_manifest
            )

        self._conn.rpc(perform)


    @property
    def launch_pad(self) -> LaunchSite:
        def perform(ctx):
            for facility in ctx.clr.PSystemSetup.Instance.SpaceCenterFacilityLaunchSites:
                if facility.name == 'LaunchPad':
                    return facility
                
            return None
        
        return self._conn.rpc(perform)
    

    @property
    def runway(self) -> LaunchSite:
        def perform(ctx):
            for facility in ctx.clr.PSystemSetup.Instance.SpaceCenterFacilityLaunchSites:
                if facility.name == 'Runway':
                    return facility
                
            return None
        
        return self._conn.rpc(perform)