import subprocess
import os, jdk
import urllib
from urllib.request import urlretrieve


class ToolKit:
    def __init__(self):
        if not os.path.exists("BuildTools.jar"):
            self.__get_build_tools()

        self.is_java_installed = self.__check_java_installation()

        if not self.is_java_installed:
            print("Java is not installed, installing...")
            self.__installjava(8)


    def __check_java_installation(self):
        print("Checking if java is installed")
        try:
            java_command_output = subprocess.run(["java  -version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                                 shell=True).stderr.decode()
        except subprocess.CalledProcessError as e:
            return False
        except Exception as e:
            print("There was an error when checking your java installation: ", end="")
            print(e)
            return False
        if not "version" in java_command_output.lower():
            return False
        return True

    def __get_build_tools(self):
        try:
            url = "https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar"
            print("Downloading build tools...")
            urlretrieve(url, "BuildTools.jar")
        except Exception as e:
            print(f"Error while downloading build tools: {e}")

    def __installjava(self, ver):
        try:
            print(f"Installing Java Runtime Environment {ver}")
            jdk.install(ver, jre=True)
            print("Done")
        except StopIteration:
            pass
        except PermissionError:
            pass

    def deleting_error(self):
        print("There was an error when deleting your files.")
        return