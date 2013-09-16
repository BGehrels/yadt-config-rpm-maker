import shutil
import os

from config_rpm_maker.hostRpmBuilder import HostRpmBuilder

class ConfigViewerAdapter(object):

    def move_configviewer_dirs_to_final_destination(self, hosts):
        for host in hosts:
            temp_path = HostRpmBuilder.get_config_viewer_host_dir(host, True)
            dest_path = HostRpmBuilder.get_config_viewer_host_dir(host)
            if os.path.exists(dest_path):
                shutil.rmtree(dest_path)
            shutil.move(temp_path, dest_path)
