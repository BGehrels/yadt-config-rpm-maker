class BaseConfigRpmMakerException(Exception):
    error_info = "Generic Error:\n"
    
    def get_error_message(self):
        return self.error_info + str(self)

class ConfigurationException(BaseConfigRpmMakerException):
    error_info = "Configuration error, please fix it\n"
