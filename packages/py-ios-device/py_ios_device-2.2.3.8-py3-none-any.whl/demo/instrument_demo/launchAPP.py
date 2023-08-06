"""
启动 app
"""
import os
import sys
from time import sleep

sys.path.append(os.getcwd())

from ios_device.servers.Instrument import InstrumentServer


def _launch_app(rpc, bundleid):
    rpc._start()

    def on_channel_message(res):
        pass
        # if 'Total' in res.auxiliaries[0]:
        #     print(res.auxiliaries[0])
        # print(res.auxiliaries[0])

    channel = "com.apple.instruments.server.services.processcontrol"
    rpc.register_channel_callback(channel, on_channel_message)
    pid = rpc.call(channel, "launchSuspendedProcessWithDevicePath:bundleIdentifier:environment:arguments:options:", "",
                   bundleid, {'DYLD_PRINT_STATISTICS': 1}, [],
                   {"StartSuspendedKey": 0, "ActivateSuspended": True, "KillExisting": 1}).selector
    print("start", pid)
    sleep(10)


if __name__ == '__main__':
    rpc = InstrumentServer().init()
    _launch_app(rpc, 'com.uanmou.aiyu')
    rpc.stop()
