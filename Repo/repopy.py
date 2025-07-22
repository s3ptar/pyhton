
"""#####################################################################
#! \file:                   repopy.py
#  \projekt:                check repository sync
#  \created on:             2025 07 18
#  \author:                 R. Gräber
#  \version:                0
#  \history:                -
#  \brief
#####################################################################"""

"""#####################################################################
# Includes
#####################################################################"""
from datetime import date
import os
import platform
import subprocess
import shutil
import logging
"""#####################################################################
# Informations
#####################################################################"""
#https://os.mbed.com/platforms/FRDM-K64F/#board-pinout
"""#####################################################################
# Declarations
#####################################################################"""
_debug_enable_ = 1
"""#####################################################################
# Constant
#####################################################################"""
const_download_folder = "/tmp/repotmp"
"""#####################################################################
# Global Variable
#####################################################################"""
filesystem_space = []
repo_id_list = []
repo_security_list = []
base_logger = logging.getLogger('RepoSyn')
str_log_format = "%(asctime)s , %(levelname)s, %(message)s, %(filename)s, %(funcName)s"
log_level = logging.DEBUG
"""#####################################################################
# local Variable
#####################################################################"""

"""#####################################################################
# Constant
#####################################################################"""

"""#####################################################################
# Local Funtions
#####################################################################"""


"""#####################################################################
#! \fn          clean_folder()
#  \brief       clean folder, and create folder if not exist
#  \param       self
#  \exception   none
#  \return      none
#####################################################################"""
def clean_folder():
    #check if folder exists
    try:
        if not os.path.exists(const_download_folder):
            base_logger.debug('folder not exist, create')
            os.mkdir(const_download_folder)
        #clean folder
    exept e:
        base_logger.error(e)
        return 0
    
    try:    
        shutil.rmtree("/tmp/repotmp/")
        os.mkdir(const_download_fWolder)
    except e
        base_logger.error(e)
        return 0


"""#####################################################################
#! \fn          detect_repolist(self)
#  \brief       detect repository list
#  \param       self
#  \exception   none
#  \return      none
#####################################################################"""
def detect_repolist():
    global repo_id_list
    if "3.6" in platform.python_version():
        result = subprocess.getoutput("yum repolist --enabled")
    #parse line by line
    result_array = result.split("\n")
    #remove header
    result_array.pop(0)
    #enumerate array to first para (index)
    for index, repo in enumerate(result_array):
        #keep only repo id
        result_array[index] = (repo.split("    ")[0])
    base_logger.debug(result_array)
    repo_id_list = result_array
    
"""#####################################################################
#! \fn          get_space_szie()
#  \brief       read directory size
#  \param       diffcalc - 0 absolute, 1 diffrenz
#  \exception   none
#  \return      none
#####################################################################"""
def get_space_szie(diffcalc):
    global filesystem_space
    if "3.6" in platform.python_version():
        #ask für file system size
        result = subprocess.getoutput("df")

"""#####################################################################
#! \fn          detect_security_list(self)
#  \brief       detect ecurity list
#  \param       self
#  \exception   none
#  \return      none
#####################################################################"""
def detect_security_list():
    global repo_security_list
    if "3.6" in platform.python_version():
        result = subprocess.getoutput("dnf updateinfo list security")
    base_logger.debug(result)
    #split
    result_array = result.split("\n")
    #remove header
    result_array.pop(0)
    for index, repo in enumerate(result_array):
        #keep only repo id
        result_array[index] = (repo.split(" ")[-1])
    #debug_out(result_array)
    repo_security_list = result_array

"""#####################################################################
#! \fn          reposync(self)
#  \brief       detect ecurity list
#  \param       self
#  \exception   none
#  \return      none
#####################################################################"""
def reposync():
    global repo_security_list
    for index, repo in enumerate(repo_security_list):
        #keep only repo id
        if "3.6" in platform.python_version():
            subprocess.getoutput("dnf download " + repo  + " --downloadonly --downloaddir=/tmp/repotmp/")
            base_logger('download {0}'.format(repo))
            
 """#####################################################################
#! \fn          init
#  \brief       start up function
#  \param       none
#  \exception   none
#  \return      none
#####################################################################"""
if __name__ == "__init__":
    
    log_file_name = 'reposyn_{0}.log'.format(x.strftime('%Y%m%d_%H%M'))
    #hdl_fileHandler = logging.FileHandler("{0}/{1}.log".format(logPath, fileName))
    hdl_fileHandler = logging.FileHandler(log_file_name)
    hdl_fileHandler.setFormatter(str_log_format)
    hdl_fileHandler.SetLevel(log_level)
    base_logger.addHandler(hdl_fileHandler)

    hdl_consoleHandler = logging.StreamHandler()
    hdl_consoleHandler.setFormatter(str_log_format)
    hdl_consoleHandler.SetLevel(log_level)
    base_logger.addHandler(hdl_consoleHandler)
    


"""#####################################################################
#! \fn          main
#  \brief       main function
#  \param       none
#  \exception   none
#  \return      none
#####################################################################"""
if __name__ == "__main__":
    base_logger.info("Python Script to debugg reposync")
    today = date.today()
    # Print the date
    base_logger.info('Date:{0} - OS:{1} - Platform:{2} - Release:{3} - VersionData:{4} - Arch:{5} - PyVersion:{6}'.format(
        today,
        os.name,
        platform.system(),
        platform.release(),
        platform.version(),
        platform.architecture(),
        platform.python_version()))


    clean_folder()
    detect_repolist()
    debug_out(repo_id_list)
    detect_security_list()
    reposync()
