from typing import List
from kspi.rpc.client import Connection



class LaunchSite:

    TYPE_TAG = 'ksp.LaunchSite'


    def __init__(self, conn: Connection, props: dict):
        self._conn = conn
        self._name = props['name']


    def __str__(self):
        return f'{self._name}'
    

    @property
    def name(self):
        return self._name


def launch_site_setup_client_side_pickling(conn: Connection):
    def pickleClientSide(obj):
        if isinstance(obj, LaunchSite):
            return (LaunchSite.TYPE_TAG, obj._name)
        else:
            return None
        
    def unpickleClientSide(pid):
        type_tag, props = pid
        if type_tag == LaunchSite.TYPE_TAG:
            return LaunchSite(conn, props)
        else:
            return None
        
    conn.pickling.register_pickler_unpickler(pickleClientSide, unpickleClientSide)


def launch_site_setup_server_side_pickling(conn: Connection):
    launch_site_type_tag = LaunchSite.TYPE_TAG

    def setup(ctx):
        def pickleServerSide(obj):
            if isinstance(obj, ctx.clr.LaunchSite):
                return (
                    launch_site_type_tag,
                    {
                        'name': obj.name
                    })
            if isinstance(obj, ctx.clr.PSystemSetup.SpaceCenterFacility):
                if obj.IsLaunchFacility():
                    return (
                        launch_site_type_tag,
                        {
                            'name': obj.name
                        })
                else:
                    return None
            else:
                return None
        
        def unpickleServerSide(pid):
            type_tag, name = pid
            if type_tag == launch_site_type_tag:
                for facility in ctx.clr.PSystemSetup.Instance.SpaceCenterFacilityLaunchSites:
                    if facility.name == 'LaunchPad' or facility.name == 'Runway':
                        return facility
                
                return ctx.clr.PSystemSetup.Instance.GetLaunchSite(name)
            else:
                return None
            
        ctx.pickling.register_pickler_unpickler(pickleServerSide, unpickleServerSide)

    conn.rpc(setup)



class System:

    def __init__(self, conn: Connection):
        self._conn = conn
        self._launch_sites = None


    @property
    def launch_sites(self) -> List[LaunchSite]:
        if self._launch_sites == None:
            self._launch_sites = self._conn.rpc(lambda ctx: [*ctx.clr.PSystemSetup.Instance.LaunchSites] + [*ctx.clr.PSystemSetup.Instance.SpaceCenterFacilityLaunchSites])

        return self._launch_sites