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
repo_id_list = []
repo_security_list = []
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
#! \fn          clean_folder(self)
#  \brief       clean folder, and create folder if not exist
#  \param       self
#  \exception   none
#  \return      none
#####################################################################"""
def debug_out(dbg_msg):
    if _debug_enable_:
        print(dbg_msg)

"""#####################################################################
#! \fn          clean_folder(self)
#  \brief       clean folder, and create folder if not exist
#  \param       self
#  \exception   none
#  \return      none
#####################################################################"""
def clean_folder():
    #check if folder exists
    if not os.path.exists(const_download_folder):
        os.mkdir(const_download_folder)
    #clean folder
    shutil.rmtree("/tmp/repotmp/")
    os.mkdir(const_download_folder)


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
    debug_out(result_array)
    repo_id_list = result_array

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
    debug_out(result)
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
            debug_out(repo)
            subprocess.getoutput("dnf download " + repo  + " --downloadonly --downloaddir=/tmp/repotmp/")


"""#####################################################################
#! \fn          main
#  \brief       start up function
#  \param       none
#  \exception   none
#  \return      none
#####################################################################"""
if __name__ == "__main__":
    print("Python Script to debugg reposync")
    today = date.today()
    # Print the date
    print("Today's date:", today)
    print("OS is:", os.name)
    print("Platform:", platform.system())
    print("Release:", platform.release())
    print("Version Date:", platform.version())
    print("Architekture:", platform.architecture())
    print("Pythonversion:", platform.python_version())

    clean_folder()
    detect_repolist()
    debug_out(repo_id_list)
    detect_security_list()
    reposync()




