from config_rpm_maker.exceptions import BaseConfigRpmMakerException
from config_rpm_maker.exceptions import ConfigurationException
import config
import subprocess

class CouldNotUploadRpmsException(BaseConfigRpmMakerException):
    error_info = "Could not upload rpms!\n"

class ConfigRpmUploader(object):
    def upload_rpms(self, rpms):
        rpm_upload_cmd = config.get('rpm_upload_cmd')
        chunk_size = self._get_chunk_size(rpms)

        if rpm_upload_cmd:
            pos = 0
            while pos < len(rpms):
                rpm_chunk = rpms[pos:pos + chunk_size]
                cmd = '%s %s' % (rpm_upload_cmd, ' '.join(rpm_chunk))
                returncode = subprocess.call(cmd, shell=True)
                if returncode:
                    raise CouldNotUploadRpmsException('Could not upload rpms. Called %s . Returned: %d'%(cmd, returncode))
                pos += chunk_size

    def _get_chunk_size(self, rpms):
        chunk_size_raw = config.get('rpm_upload_chunk_size', 0)
        try:
            chunk_size = int(chunk_size_raw)
        except ValueError as e:
            raise ConfigurationException('rpm_upload_chunk_size (%s) is not a legal value (should be int)'%chunk_size_raw)
        if chunk_size < 0:
            raise ConfigurationException("Config param 'rpm_upload_cmd_chunk_size' needs to be greater or equal 0")

        if not chunk_size:
            chunk_size = len(rpms)

        return chunk_size
