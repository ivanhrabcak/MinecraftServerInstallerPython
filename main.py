#!/bin/python
import os, sys, shutil, subprocess, json, jdk, math
from psutil import virtual_memory
import urllib
from urllib.request import urlretrieve

def SetOption(key, value):
    if not os.path.exists("server.properties"):
        return
    f = open("server.properties", "r")
    data = f.read()
    f.close()

    options = []
    lines = data.split("\n")
    for line in lines:
        if not line.startswith("#"):
            options.append(line)
    
    new_options = []
    for option in options:
        if option == "":
            continue
        option_key_value = option.split("=")
        if option_key_value[0] == key:
            option_key_value[1] = value
        if len(option_key_value) != 1:
            new_options.append(option_key_value[0] + "=" + option_key_value[1])
        else:
            new_options.append(option_key_value[0] + "=")

    output = ""
    for option in new_options:
        output += option + "\n"

    f = open("server.properties", "w+")
    f.write(output)
    f.close()       

def EditEula():
    if not os.path.exists("eula.txt"):
        return
    f = open("eula.txt", "r")
    data = f.read()
    f.close()
    data = data.replace("false", "true")
    f = open("eula.txt", "w+")
    f.write(data)
    f.close()

def FetchBuildTools():
    if os.path.exists("BuildTools.jar"):
        print("Build tools downloaded, not downloading.")
        return

    try:
        url = "https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar"
        print("Downloading build tools...")
        urlretrieve(url, "BuildTools.jar")
    except Exception as e:
        print("Error while downloading build tools: %s" % (str(e)))

def InstallJava(ver):
    try:
        print(f"Installing Java Runtime Environment {ver}")
        jdk.install(ver, jre=True)
        print("Done")
    except StopIteration:
        pass
    except PermissionError:
        pass

def CheckJavaInstallation():
    print("Checking if java is installed")
    try:
        java_command_output = subprocess.run(["java  -version"], stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell=True).stderr.decode()
    except subprocess.CalledProcessError as e:
        return False
    except Exception as e:
        print("There was an error when checking your java installation: ", end = "")
        print(e)
        return False
    if not "version" in java_command_output.lower():
        return False
    return True

def InstallServer(ver):
    curr_dir = os.getcwd()
    print("Do you want to install in current directory? (y/n)")
    print(f"{curr_dir} - is your current directory")
    install_in_curr_dir = input("? ")

    if install_in_curr_dir.lower() == "y":
        print("Installing...")
        os.system("java -jar BuildTools.jar --rev %s" % (ver))
        print("Installing stopped...")
    elif install_in_curr_dir.lower() == "n":
        user_dir = input("Your Directory: ")
        os.chdir(user_dir)
        print("Installing...")
        os.system(f"java -jar BuildTools.jar --rev %s" % (ver))
    else:
        print("Bad option")
        InstallServer(ver)
        return
    cracked_minecraft = input("Do you or your friends have cracked minecraft (this will turn off online mode)? ")
    
    if cracked_minecraft.lower() == "y":
        print("Overwriting server.properties")
        SetOption("online-mode", "false")

def UpdateServer(ver):
    print("Updating")
    os.system(f"java -jar BuildTools.jar --rev %s" % (ver))
    Menu()

def DeletingError():
    print("There was an error when deleting your files.")
    return

def DeleteServer():
    print("Where are your server files located? (type the whole path to directory)")
    dir_for_data = input("? ")
    print(f"Are you sure you want do delete your whole server? This action can't be undone (y/n)")
    dele = input("? ")
    if dele == "y":
        shutil.rmtree(dir_for_data, ignore_errors = True, onerror = DeletingError)
        Menu()
    else:
        Menu()

def RunServer(ver):
    EditEula()
    print("Run server?  (y/n)")
    run = input("? ")

    if run == "y":
        memory = math.floor(virtual_memory().total * pow(10, -9) )
        print("Allocating half of memory - %dGB" % (memory))
        os.system('java -Xmx%dG -Xms%dG -jar spigot-%s.jar -nogui' % (memory, memory, ver))
        Menu()
    else:
        print("Wrong input, going back to menu...")
        Menu()
    Menu()

def Menu():
    FetchBuildTools()
    is_java_installed = CheckJavaInstallation()
    if not is_java_installed:
        InstallJava(8) # 8 is the minimum for a minecraft server
    print(" What do you want to do?")
    print("\n")
    print("[0] -- Install server")
    print("[1] -- Run Server")
    print("[2] -- Update Server")
    print("[3] -- DELETE SERVER")

    choice = input("? ")

    if choice == "0":
        InstallServer(input("Version? "))
    elif choice == "1":
        RunServer(input("Version? "))
    elif choice == "2":
        UpdateServer(input("Version? "))
    elif choice == "3":
        DeleteServer()

if __name__ == "__main__":
    Menu()
