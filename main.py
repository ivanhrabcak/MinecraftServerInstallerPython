import subprocess
import os, jdk, json
import urllib, requests
from urllib.request import urlretrieve
import math
from psutil import virtual_memory


class Utils:
    def __init__(self):
        if not os.path.exists("BuildTools.jar"):
            self.__get_build_tools()

        self.is_java_installed = self.__check_java_installation()

        if not self.is_java_installed:
            print("Java is not installed, installing...")
            self.__installjava(8)

    @staticmethod
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

    @staticmethod
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

    def edit_eula(self):
        if not os.path.exists("eula.txt"):
            return
        f = open("eula.txt", "r")
        data = f.read()
        f.close()
        data = data.replace("false", "true")
        f = open("eula.txt", "w+")
        f.write(data)
        f.close()



class ServerUtils:
    def __init__(self):
        self.current_dir = os.getcwd()
        self.utils = Utils()

    def get_mc_version(self):
        self.raw_json_data = requests.get(
            "https://launchermeta.mojang.com/mc/game/version_manifest.json").content.decode()       #LOL this stooopid fast
        self.json_loaded_data = json.loads(self.raw_json_data)
        self.newest_mc_version = self.json_loaded_data.get("latest").get("release")

    def install_server(self):
        print("Do you want to install in current directory? (y/n)")
        print(f"{self.current_dir} - Is your current directory")
        self.install_in = input("? ")
        print("Do you want to install newest version of Minecraft? (y/n)")
        install_newest_mc_version = input("? ")


        if self.install_in.lower() == "y" and install_newest_mc_version.lower() == "y":         #FIXME
            print("Installing...")                                                              #Should add getting of the version into menu()
            os.system(f"java -jar BuildTools.jar --rev {self.newest_mc_version}")
            print("Installing stopped...")
            return self.newest_mc_version

        elif self.install_in.lower() == "y" and install_newest_mc_version.lower() == "n":       #FIXME
            self.version = input("Version? \n ? ")
            print(f"Installing Minecraft version {self.version}...")
            os.system(f"java -jar BuildTools.jar --rev {self.version}")
            print("Installing stopped...")
            return self.version

        elif self.install_in.lower() == "n" and install_newest_mc_version.lower() == "y":      #FIXME
            user_dir = input("Your Directory: ")
            os.chdir(user_dir)
            print(f"Sucesfully changed to {os.getcwd()}")
            print(f"Installing Minecraft version {self.newest_mc_version}...")
            os.system(f"java -jar BuildTools.jar --rev {self.newest_mc_version}")
            return self.newest_mc_version

        elif self.install_in.lower() == "n" and install_newest_mc_version.lower() == "n":      #FIXME
            user_dir = input("Your Directory: ")
            os.chdir(user_dir)
            print(f"Sucesfully changed to {os.getcwd()}")
            version = input("Version? \n ? ")
            print(f"Installing Minecraft version {version}...")
            os.system(f"java -jar BuildTools.jar --rev {version}")
            return self.version

    def run_server(self, version):

        self.utils.edit_eula()

        print("Run server?  (y/n)")
        run = input("? ")

        if run == "y":
            memory = math.floor(virtual_memory().total * pow(10, -9))
            os.system('java -Xmx%dG -Xms%dG -jar spigot-%s.jar -nogui' % (memory, memory, version))

        else:
            print("Wrong input, going back to menu...")


def Menu():
    srv_util = ServerUtils()
    print(" What do you want to do?")
    print("\n")
    print("[0] -- Install server")
    print("[1] -- Run Server")
    print("[2] -- Update Server")
    print("[3] -- DELETE SERVER")

    choice = input("? ")

    if choice == "0":
        global installed_version
        installed_version = srv_util.install_server()
    elif choice == "1":
        srv_util.run_server(installed_version)      #FIXME