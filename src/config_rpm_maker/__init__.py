from config_rpm_maker.configRpmMaker import ConfigRpmMaker
from config_rpm_maker.configRpmUploader import ConfigRpmUploader
from config_rpm_maker.configViewerAdapter import ConfigViewerAdapter
from config_rpm_maker.svn import SvnService
from config_rpm_maker.exceptions import BaseConfigRpmMakerException
from config_rpm_maker import config

import logging
import traceback
import sys


logging.basicConfig(
    format="%(asctime)s %(levelname)5s [%(name)s] - %(message)s",
    level=config.get('log_level', 'INFO'),
)




class CliException(BaseConfigRpmMakerException):
    error_info = "Command Line Error:\n"

def mainMethod(args=sys.argv[1:]):
    try:
        if len(args) != 2:
            raise CliException("You need to provide 2 parameters (repo dir, revision).\nArguments were %s " % str(args))
    
        if not (args[1].isdigit() and int(args[1]) >= 0):
            raise CliException("Revision must be a positive integer.\nGiven revision was '%s'" % args[1])
        
    # first use case is post-commit hook. repo dir can be used as file:/// SVN URL
        svn_service = SvnService(
            base_url = 'file://' + args[0],
            path_to_config = config.get('svn_path_to_config')
        )
        config_rpm_maker = ConfigRpmMaker(revision=args[1], svn_service=svn_service)
        result = config_rpm_maker.build()
        ConfigRpmUploader().upload_rpms(result.rpms)
        ConfigViewerAdapter().move_configviewer_dirs_to_final_destination(result.affectedHosts)
        config_rpm_maker.clean_up()
    except (BaseConfigRpmMakerException) as e:
        print "See the error log for details."
        sys.exit(1)
    except Exception:
        traceback.print_exc(5)
        sys.exit(2)