import sys
import logging

from pyhomematic import _hm

LOG = logging.getLogger(__name__)


class HMConnection(object):
    def __init__(self,
                 local=_hm.LOCAL,
                 localport=_hm.LOCALPORT,
                 remote=_hm.REMOTE,
                 remoteport=_hm.REMOTEPORT,
                 devicefile=_hm.DEVICEFILE,
                 interface_id=_hm.INTERFACE_ID,
                 autostart=False,
                 eventcallback=False,
                 systemcallback=False,
                 resolvenames=False,
                 resolveparamsets=False,
                 rpcusername=_hm.RPC_USERNAME,
                 rpcpassword=_hm.RPC_PASSWORD):
        """
        Helper function to quickly create the server thread to which the CCU / Homegear will emit events.
        Without specifying the remote data we'll assume we're running Homegear on localhost on the default port.
        """
        LOG.debug("HMConnection: Creating server object")

        # Device-storage
        self.devices = _hm.devices
        self.devices_all = _hm.devices_all
        self.devices_raw = _hm.devices_raw
        self.devices_raw_dict = _hm.devices_raw_dict

        try:
            self._server = _hm.ServerThread(local=local,
                                            localport=localport,
                                            remote=remote,
                                            remoteport=remoteport,
                                            devicefile=devicefile,
                                            interface_id=interface_id,
                                            eventcallback=eventcallback,
                                            systemcallback=systemcallback,
                                            resolvenames=resolvenames,
                                            rpcusername=rpcusername,
                                            rpcpassword=rpcpassword,
                                            resolveparamsets=resolveparamsets)

        except Exception as err:
            LOG.critical("Failed to create server")
            LOG.debug(str(err))

        if autostart:
            self.start()

    def start(self, *args, **kwargs):
        """
        Start the server thread if it wasn't created with autostart = True.
        """
        if args:
            LOG.debug("args: %s" % str(args))
        if kwargs:
            LOG.debug("kwargs: %s" % str(kwargs))
        try:
            self._server.start()
            self._server.proxyInit()
            return True
        except Exception as err:
            LOG.critical("Failed to start server")
            LOG.debug(str(err))
            self._server.stop()
            return False

    def stop(self, *args, **kwargs):
        """
        Stop the server thread.
        """
        if args:
            LOG.debug("args: %s" % str(args))
        if kwargs:
            LOG.debug("kwargs: %s" % str(kwargs))
        try:
            self._server.stop()
            self._server = None

            # Device-storage clear
            self.devices.clear()
            self.devices_all.clear()
            self.devices_raw.clear()
            self.devices_raw_dict.clear()

            return True
        except Exception as err:
            LOG.critical("Failed to stop server")
            LOG.debug(str(err))
            return False

    def getAllSystemVariables(self):
        """Get all system variables from CCU / Homegear"""
        if self._server is not None:
            return self._server.getAllSystemVariables()

    def getSystemVariable(self, name):
        """Get single system variable from CCU / Homegear"""
        if self._server is not None:
            return self._server.getSystemVariable(name)

    def deleteSystemVariable(self, name):
        """Delete a system variable from CCU / Homegear"""
        if self._server is not None:
            return self._server.deleteSystemVariable(name)

    def setSystemVariable(self, name, value):
        """Set a system variable on CCU / Homegear"""
        if self._server is not None:
            return self._server.setSystemVariable(name, value)

    def getServiceMessages(self):
        """Get service messages from CCU / Homegear"""
        if self._server is not None:
            return self._server.getServiceMessages()

    def rssiInfo(self):
        """Get RSSI information for all devices from CCU / Homegear"""
        if self._server is not None:
            return self._server.rssiInfo()

    def setInstallMode(self, on=True, t=60, mode=1, address=None):
        """Activate or deactivate installmode on CCU / Homegear"""
        if self._server is not None:
            return self._server.setInstallMode(on, t, mode, address)

    def getInstallMode(self):
        """Get remaining time in seconds install mode is active from CCU / Homegear"""
        if self._server is not None:
            return self._server.getInstallMode()

    def getAllMetadata(self, address):
        """Get all metadata of device"""
        if self._server is not None:
            return self._server.getAllMetadata(address)

    def getMetadata(self, address, key):
        """Get metadata of device"""
        if self._server is not None:
            return self._server.getAllMetadata(address, key)

    def setMetadata(self, address, key, value):
        """Set metadata of device"""
        if self._server is not None:
            return self._server.getAllMetadata(address, key, value)

    def deleteMetadata(self, address, key):
        """Delete metadata of device"""
        if self._server is not None:
            return self._server.deleteAllMetadata(address, key)

    def listBidcosInterfaces(self):
        """Return all available BidCos Interfaces"""
        if self._server is not None:
            return self._server.listBidcosInterfaces()
