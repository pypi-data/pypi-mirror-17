__author__ = 'CoYe'

from abc import ABCMeta
from abc import abstractmethod

class NetworkingResourceDriverInterface:
    __metaclass__ = ABCMeta

    @abstractmethod
    def ApplyConnectivityChanges(self, context, request):
        pass

    @abstractmethod
    def send_custom_command(self, context, custom_command):
        pass

    @abstractmethod
    def send_custom_config_command(self, context, custom_command):
        pass

    @abstractmethod
    def save(self, context, folder_path, configuration_type, vrf_management_name=None):
        pass

    @abstractmethod
    def restore(self, context, path, configuration_type='running', restore_method='override', vrf_management_name=None):
        pass

    @abstractmethod
    def update_firmware(self, context, remote_host, file_path):
        pass

    @abstractmethod
    def get_inventory(self, context):
        pass

    @abstractmethod
    def orchestration_restore(self, context, saved_artifact_info, custom_params=None):
        pass

    @abstractmethod
    def orchestration_save(self, context, mode="shallow", custom_params=None):
        pass

    @abstractmethod
    def health_check(self, context):
        pass

    @abstractmethod
    def load_firmware(self, context, path, vrf_management_name=None):
        pass

    @abstractmethod
    def shutdown(self, context):
        pass
