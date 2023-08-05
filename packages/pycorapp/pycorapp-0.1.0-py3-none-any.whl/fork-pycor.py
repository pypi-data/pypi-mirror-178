
# PyCor v1.13.0 / Server 1026 SOURCE CODE

# LIB IMPORTS
from asyncio import ensure_future
from subprocess import run
from turtle import update
from webbrowser import open_new_tab
from sys import path_hooks
from sys import path
from webbrowser import open_new
from json import encoder
encoder.py_encode_basestring
# REGISTRYBUILTINVALUES
InstallDir="REG_SZ: C:\\Users\\Admin\\"
#ACTIVATION
def activate_pycor():
  callable = True
  grubcommons = 1
  grubpcbin = 1
  nasm = 1
  xorriso = 1
  aptgetupdate = 1
  aptgetupgrade = 1
  shellget = 0
  pycor = 1
  alljslibs = 0
  robotstxt = 0
  websiteadded = 1
  aptgetupdatent = 1
  defer = 0
activate_pycor()
# BEFORE START

# User content
#print("pycor info: OCCW is loading...")
#print("pycor info: Running pycor.py...")
#print("pycor info: Building OEM scripts...")
#print("pycor info: Loading CLI tool...")
#print("pycor info: Locating file scripts...")
#print("pycor info: Analysing base_library.zip...")
#print("pycor info: Daemon is loading...")
#print("pycor info: Running program...")
#print("--------------------------------------------------------------------------------------------")
# Runner scripts
#from pycor import *
#Ustart = 1
#pycor = {
#    "name": "pycor.py",
#  "version": "null"
#}


#def pycor_runner():
#  runner = pycor
#  runner = "cli"
#  runner = "exe"
#  runner = "null"
#  runner = "/root/daemon"
#  runner = "/root/buildenv"
#  runner = "/root/regkeys"
#  runner = "/root/runners"
#  runner = "script.parent"

#pycor_runner.start(startState = "advanced", instances = 1)
#pycor_runner.state = "developer"

# METADATA
packagefile = "js:package.json src = 'root/package.json' defer"
# INNO SETUP COMPILER DATA
AppName={"#MyAppName"}
AppVer="v1.xy.z"
ISSFile={"TSCLIENT1/ISSFiles/iss.iss"}

# SOURCE CODE
print("Welcome to PyCor 1.13.0.1027 LTS 15 Beta")
print("Type help_pycor for help")
x = ""
while x != "0":
    x = input(">> ")

    cmd1 = "PyCor Objects: In device's memory. Will reset when restarted"
    if x == str("other_vbc"):
        print("[1] package.json")
        while x != "0":
            x = input("Select to view: ")
            if x == "1":
                print("""
                      {
    "target": "pycor.py",
    "name": "pycor",
    "version": "1.12.2",
    "description": "An official PyCor package for both Node.js and npm uses. Synced version with software version",
    "main": "index.js",
    "scripts": {
      "test": "pycor run prg"
    },
    "dependencies": {
      "fastify": "^4.9.2",
      "handlebars": "^4.7.7",
      "@fastify/formbody": "^7.3.0",
      "@fastify/static": "^6.5.0",
      "@fastify/view": "^7.1.2",
      "node": "^19.0.1",
      "pycor": "^1.0.1"
    },
    "repository": {
      "type": "git",
      "url": "git+https://github.com/UnknownUser2222/pycor.git"
    },
    "author": "UnknownUser2222",
    "license": "MIT",
    "bugs": {
      "url": "https://github.com/UnknownUser2222/pycor/issues"
    },
    "homepage": "https://github.com/UnknownUser2222/pycor#readme",
    "keywords": [
      "pycor"
    ],
    "pycor_readinfo": {
       "epc": [{
        "resource": "/c:/Users/Admin/Desktop/gitpy2/package.json",
        "owner": "_generated_diagnostic_collection_name_#1",
        "code": "768",
        "severity": 4,
        "message": "Problems loading reference 'https://json.schemastore.org/package': Unable to load schema from 'https://json.schemastore.org/package': getaddrinfo ENOTFOUND json.schemastore.org.",
        "startLineNumber": 1,
        "startColumn": 1,
        "endLineNumber": 1,
        "endColumn": 2
      }]
    }
  }

                     """)
    elif x == str("redirect_pycorwebsite"):
        
        if x == False:
            print("EOF")
        else:
            print("Sorry, this version does not support inputs. Please select a website below:")
            print("[1] webqa.com/pycor/Connect/?platform=cli&website=pycorweb.com/pycor/cmb#cli")
            webinput = input("Website (PyCor): ")
            if webinput == "1":
              print("Connected to pycor.glitch.me/app@pycor#cli?mode=fullcontrol")
              print("......................................................................................")
              print(" Welcome to PyCor's official website! From the CLI!")                
              print(" We have a variety of options to do (including local actions) Select one from below!")
              print(" [0] Exit [1] Print some text [2] Open a website")
              print("")
              print(" To select an option type a valid number and hit Enter. It will not bring the next page as long there is a valid character.")
              print(" How is it connecting even when I'm offline? Well, it is saved as a download until you connect to the Internet again.")
              print(" [3] Repository [4] Official website")
              print(" Website by github.com/UnknownUser1836")
             
              while x != "0":
              
               x = input("Press Enter to view next page")
               if x == "1":
                tempInput = input("Text to print: ")
                print(tempInput)
               if x == "2":
                tempInput = input("Website: ")
                open_new_tab(tempInput)
               if x == "3":
                open_new_tab("https://github.com/UnknownUser2222/pycor")
               if x == "4":
                open_new_tab("https://pycor.glitch.me")
               if x == "":
                print("No newline available. To exit, type 0")
    elif x == str("update pycor"):
        print("        Name           Version               Size")
        print("[1] PyCor 1.06.9 Beta  v1.06.9               2KB")
        print("Press a key to upgrade to")
        updateoption = input("Option:")
        if updateoption == "1":
            print("pycor info: Downloading files... 100%")
            print("pycor info: Installing files... 100%")
            print("pycor info: Assigning file root... 100%")
            print("pycor info: Updating component registry... 100%")
            print("pycor info: Assigning file values... 100%")
            print("pycor info: Updating destination path... 100%")
            print("pycor info: Updating bug fixes... 100%")
            print("Update complete")

        
    elif x == str("help_pycor"):
        print("Website Opener commands")
        print("redirect - Goes to a website with default browser.")
        print("redirect_pycorwebsite - Redirects to a PyCor website (must contain pycor_manifest.json)")
        print("PyCor Commands")
        print("add_object - Adds a object to the list")
        print("list_objects - Shows the list of objects")
        print("add_key - Adds a key to the registry")
        print("add_python_key - Adds a Python variable if an 'object' does not work")
        print("add_script - Adds a Python script")
        print("remove_object - Removes an object.")
        print("remove_python_key - Deletes a Python key.")
        print("remove_key - Deletes a key")
        print("remove_script - Removes a script.")
        print("add_python_object - Adds a Python object.")
        print("add_pycor_variable - Adds a PyCor variable.")
        print("add_jscript_variable - Adds a JavaScript variable")
        print("remove_python_object - Removes a Python object")
        print("client_redirect_host - Redirects to host server")
        print("connect_to_github_server - Connects to a GitHub repository")
        print("drive_change - Changes the disk drive directory")
        print("list_version - Shows all the versions of the program installed")
        print("change_program_cmds - Changes the commands of the program (except current built-in commands)")
        print("change_pcr_regedit - Changes the registry values for a PCR file")
        print("update_pcr - Updates the current PCR file")
        print("repair_pcr - Repairs the current PCR file")
        print("add_iso - Mounts a ISO file")
        print("create_fsc - Creates a FSC file")
        print("lts_edit - Edits a LTS module selected")
        print("exp_change - Changes the EXP module")
        print("refresh_pycor - Passes a refresh")
        print("exit - Exits the program")
        print("exit_bst - Exits the BST")
        print("exit_client - Exits the client")
        print("PyCorMgr - Runs PyCorMgr.pcr")
        print("install_optional_program - Installs optional features and programs")
        print("website - Opens the official website for PyCor")
        print("other_vbc - Other items")
    elif x == str("PyCorMgr"):
        print("----------------------------------------------------------------------------------------")
        print("|                            PyCor Manager v1.1.0                                      |")
        print("|                            Select a item to run                                      |")
        print("|  [1] Exit   [2] Add file    [3] Add ISO   [4] Add root file  [5] Add package         |")
        print("|  [6] Add shell root [7] Add config [8] Add PYW file [9] View all commands            |")
        print("|                       Press any key to switch to CLI mode                            |")
        print("|______________________________________________________________________________________|")
        while x != "0":
            x = input("""app@pycor: ~su: github.com/UnknownUser2222/pycor 
 $ """)
            if x == "1":
                print("Exiting...")
                exit("""EXIT: At package line 3, exit confirmed by PyCorMgr.pcr, Codename is x-success
Trace module became <eof> interrupted by exit key.
PYCOR_MGR_0""")
                exit(-193847291)
            if x == "2":
                input("Name: ")
                input("Directory: ")
            if x == "3":
                input("Name: ")
                input("Directory: ")
            if x == "4":
                input("Name: ")
                input("Directory: ")
            if x == "5":
                input("Name: ")
                input("Directory: ")
            if x == "6":
                input("Name: ")
                input("Directory: ")
            if x == "7":
                input("Name: ")
                input("Directory: ")
            if x == "8":
                input("Name: ")
                input("Directory: ")
            if x == "9":
                print("ALL COMMANDS")
                print("[10] Add TSCript file")
                print("[11] Login to GitHub")
            if x == "10":
                input("Name: ")
                input("Directory: ")
            if x == "11":
                print("How would you login to?")
                print("[1] GitHub.com [2] GitHub Enterprise")
                x = input("Option: ")
                if x == "1":
                    github_username = input("GitHub Username: ")
                    github_password = input("GitHub Password: ")
                    print("Logging in to " + github_username)
                    print("Logged in as " + github_username)
                if x == "2":
                    github_username = input("GitHub Username: ")
                    github_password = input("GitHub Password: ")
                    print("Logging in to " + github_username)
                    print("Logged in as " + github_username)
            else:

                print("PyCor CLI - Type help for commands")
                while x != "0":
                    input("app@pycor: ")

                    if x == "help":
                        print("pycor --add file - Adds a file to the CLI.")
                    elif x == "pycor --add file":
                        input("Name and directory (separate with commas):")
                    else:
                        print("Invalid command")
    elif x == str("website"):
        open_new_tab("https://github.com/UnknownUser2222/pycor/releases/")
    elif x == str("exit_client"):
        exit(0)
    elif x == str("exit_bst"):
        exit(1)
    elif x == str("exit"):
        exit(0)
    elif x == str("install_optional_program"):
        print("      Name                      Version          Size        Publisher")
        print("[1] Website Opener               v1.00          1.21KB        PyCor")
        print("[2] PyCorMgr Dev                 v1.2.01        1.01KB        PyCor")
        print("[3] Python (VSCODE extension)    v2022.10.1     108MB        Microsoft")
        print("[4] Pylance (VSCODE extension)   v2022.10.31    199MB        Microsoft")
        print("        Press 0 to switch to marketplace apps and features         ")
        while x != "0":   
            x = input("Option: ")
            if x == "0":
                print("Type S to search")   
                while x != "1":
                 x = input("Option: ")
                 if x == "S" or x == "s":
                    searchQuery = input("Search query: ")
                    print("ERR: Traceback on module 5, missing parts 'pycorsearchquery.exe' and 'pycorstrandics.exe'. It appears that 2 files have been moved, deleted, or could'nt access. Error code: 403 FORBIDDEN -- Version: v1.07.8")
            if x == "1":
               print("Install now? Y/N")
            if x == "Y" or x == "y":
               print("Installing app...")
               print("Adding core dependencies...")
               print("Default is set to C drive; Installing on C:/Program Files (x86)/PyCor/Optional_Programs_and_Features...")
               print("Downloading runtime module from app@pycor/runtime/modules/modules-compressed.zip...")
               print("Installing program code...")
               print("Installation has been complete")
            if x == "2":
               print("Install now? Y/N")
               if x == "Y" or x == "y":
                 print("Installing app...")
                 print("Adding core dependencies...")
                 print("Default is set to C drive; Installing on C:/Program Files (x86)/PyCor/Optional_Programs_and_Features...")
                 print("Downloading runtime module from app@pycor/runtime/modules/modules-compressed.zip...")
                 print("Installing program code...")
                 print("Installation has been complete")
            if x == "3":      
               print("Install now? Y/N")
            if x == "Y" or x == "y":
               print("Installing app...")
               print("Adding core dependencies...")
               print("Default is set to C drive; Installing on C:/Program Files (x86)/PyCor/Optional_Programs_and_Features...")
               print("Downloading runtime module from app@pycor/runtime/modules/modules-compressed.zip...")
               print("Installing program code...")
               print("Installation has been complete. All parts are not installed but will be installed in 5 mins")
            if x == "4":
               print("Install now? Y/N")
               if x == "Y" or x == "y":
                    print("Installing app...")
                    print("Adding core dependencies...")
                    print("Default is set to C drive; Installing on C:/Program Files (x86)/PyCor/Optional_Programs_and_Features...")
                    print("Downloading runtime module from app@pycor/runtime/modules/modules-compressed.zip...")
                    print("Installing program code...")
                    print("Installation has been complete. All parts are not installed but will be installed in 5 mins")
          

    elif x == str("refresh_pycor"):
        print("Refreshed program.")
    elif x == str("redirect"):
        website = input("Website: https://")
        open_new_tab(website)
    elif x == str("exp_change"):
        input("Name: ")
        print("Successfully changed module.")
    elif x == str("lts_edit"):
        input("Value: ")
        print("Successfully changed values.")
    elif x == str("create_fsc"):
        input("Name: ")
        print("Successfully created FSC file.")
    elif x == str("change_pcr_regedit"):
        input("Directory: ")
        print("Successfully mounted ISO file.")
    elif x == str("repair_pcr"):
        print("Checking for errors...")
        print("Repairing...")
        print("Successfully repaired.")
    elif x == str("update_pcr"):
        print("Checking for updates")
        print("Successfully updated current file")
    elif x == str("change_pcr_regedit"):
        input("Name: ")
        input("Value: ")
        print("Successfully changed values")
    elif x == str("update_pcr"):
        print("Version: 1.02.0 Build 1003")
    elif x == str("change_program_cmds"):
        file_name = input("Name of extension/PCR file: ")
        directory = input("Directory: ")
        print("Enabling " + file_name + "'s features...")
        print("Disabling current commands (except PyCor commands)...")
        print("Checking version of file...")
        print("Enabling commands...")
        print("Successfully switched program mode")
    elif x == str("drive_change"):
        drive = input("Drive letter: ")
        print("Changed from this directory to " + drive)
    elif x == str("connect_to_github_server"):
        input("Name of repo: ")
        input("Owner or organization: ")
        print("Successfully joined server.")
    elif x == str("client_redirect_host"):
        input("Name of server: ")
        input("Directory: ")
        print("Successfully joined server.")
    elif x == str("remove_python_object"):
        input("Name: ")
        print("Successfully removed object.")
    elif x == str("add_jscript_variable"):
        input("Name: ")
        input("Value: ")
        print("Successfully added JScript object")
    elif x == str("add_script"):
        input("Function name: ")
        input("Function code: {__one_line_script: ")
        print("Script saved successfully")
    elif x == str("remove_object"):
        input("Name: ")
        print("Successfully removed object")

    elif x == str("remove_script"):
        input("Name: ")
        print("Successfully removed script.")

    elif x == str("add_python_object"):
        input("Name: ")
        input("Value: ")
        print("Successfully added object")

    elif x == str("add_pycor_variable"):
        input("Name: ")
        print("Successfully added variable")
    elif x == str("remove_key"):
        input("Name: ")
        print("Successfully removed key")
    elif x == str("add_python_key"):
        print("Python keys can be useful if an 'object' does not work.")
        input("Name: ")
        input("Value: ")
        print("Successfully added Python key")
    elif x == str("remove_python_key"):
        input("Name: ")
        print("Successfully deleted")
    elif x == str("list_objects"):
        print(cmd1)
    elif x == str("add_key"):
        input1 = input(
            "WARNING: Adding keys without a reason might require a reinstall. Are you sure do you want to continue? ([Y]es or [N]o)")
        if input1 == "Y":
            key_name = input("Key name: ")
            key_type = input("Key type: ")
            key_value = input("Key value: ")
            print("Key " + key_name + " with type " + key_type + " as " + key_value + " successfully added to registry")
    elif x == str("add_object"):

        cmd2_1 = input("Name: ")
        cmd2_2 = input("Value: ")
        print("Successfully added to dictionary")
        print(cmd1)
    elif x == str(""):
        key = True

    else:
        print("This term is not a command or a script. Please check if you have any typos in the scripts you typed.")
# OTHER DATA
def pycor(stc):
    pycor.codespaces = 1
# spc package data
package = {
    "target": "pycor.py",
    "name": "pycor",
    "version": "1.12.2",
    "description": "An official PyCor package for both Node.js and npm uses. Synced version with software version",
    "main": "index.js",
    "scripts": {
      "test": "pycor run prg"
    },
    "dependencies": {
      "fastify": "^4.9.2",
      "handlebars": "^4.7.7",
      "@fastify/formbody": "^7.3.0",
      "@fastify/static": "^6.5.0",
      "@fastify/view": "^7.1.2",
      "node": "^19.0.1",
      "pycor": "^1.0.1"
    },
    "repository": {
      "type": "git",
      "url": "git+https://github.com/UnknownUser2222/pycor.git"
    },
    "author": "UnknownUser2222",
    "license": "MIT",
    "bugs": {
      "url": "https://github.com/UnknownUser2222/pycor/issues"
    },
    "homepage": "https://github.com/UnknownUser2222/pycor#readme",
    "keywords": [
      "pycor"
    ],
    "pycor_readinfo": {
       "epc": [{
        "resource": "/c:/Users/Admin/Desktop/gitpy2/package.json",
        "owner": "_generated_diagnostic_collection_name_#1",
        "code": "768",
        "severity": 4,
        "message": "Problems loading reference 'https://json.schemastore.org/package': Unable to load schema from 'https://json.schemastore.org/package': getaddrinfo ENOTFOUND json.schemastore.org.",
        "startLineNumber": 1,
        "startColumn": 1,
        "endLineNumber": 1,
        "endColumn": 2
      }]
    }
  }
  #inno
yes = 1
no = 0
#define MyAppName "PyCor"
#define MyAppVersion "1.13.6.1025"
#define MyAppPublisher "PyCor Incorparated"
#define MyAppExeName "pycor.exe"
#define MyAppAssocName MyAppName + " File"
#define MyAppAssocExt ".pcr"
#define MyAppAssocKey StringChange(MyAppAssocName, " ", "") + MyAppAssocExt
#define MyRegistryFileName "PYCOR_REGISTRY.REG"
#define MyLicenseFile "C:\Users\Admin\3D Objects\license.txt"
#define MyShellFile "C:\Users\Admin\Documents\PyCor\output\pycorinteractiveshell.exe"
setup = ["Setup"]
AppId={{"A0C7E541-6B17-471B-9957-F2E3F3838164"}}
AppName={"#MyAppName"}                                                                                                                                   
AppVersion={"#MyAppVersion"}
AppVerName={"#MyAppVersion"}
AppPublisher={"#MyAppPublisher"}
DefaultDirName="{autopf}/{#MyAppName}"
ChangesAssociations=yes
DefaultGroupName={"#MyAppName"}
AllowNoIcons=yes
RestartIfNeededByRun=yes
AllowUNCPath=yes
AlwaysRestart=no
LicenseFile={"#MyLicenseFile"}
AllowCancelDuringInstall=no
AllowNetworkDrive=yes
PrivilegesRequiredOverridesAllowed="dialog"
OutputBaseFilename="pycorsetup"
Compression="lzma"
SolidCompression=yes
WizardStyle="modern"
MergeDuplicateFiles=no


Langs = ["Languages"]
Name = "english"; MessagesFile = "compiler:Default.isl"
Tasks = ["Tasks"]
Name = "desktopicon"; Description = "{cm:CreateDesktopIcon}"; GroupDescription = "{cm:AdditionalIcons}"; Flags = "unchecked"

Files = ["Files"]
Source = "C:/Users/Admin/Documents/PyCor/output/dist/pycor/pycor.exe"; DestDir = "{app}"; Flags = "ignoreversion"
Source = "C:/Users/Admin/Documents/PyCor/output/dist/pycor/*"; DestDir = "{app}"; Flags = "ignoreversion, recursesubdirs, createallsubdirs"
Source = "C:/Users/Admin/Documents/PYCOR_REGISTRY.REG"; DestDir = "C:/PyCor/Registry/"; Flags = "ignoreversion"
Source = "C:/Users/Admin/Documents/PyCor/Output/pycor.py"; DestDir = "C:/"
Source = "{#MyShellFile}; DestDir: '{'app'}/'shell'/package"; Flags = "ignoreversion"
# NOTE: Don't use "Flags: ignoreversion" on any shared system files
string = "string"
HKA = 1
registry = ["Registry"]
Root = HKA; Subkey= "Software/Classes/{#MyAppAssocExt}/OpenWithProgids"; ValueType= string; ValueName= "{#MyAppAssocKey}"; ValueData= ""; Flags= "uninsdeletevalue"
Root = HKA; Subkey= "Software/Classes/{#MyAppAssocKey}"; ValueType= string; ValueName= string; ValueData= "{#MyAppAssocName}"; Flags= "uninsdeletekey"
Root = HKA; Subkey= "Software/Classes/{#MyAppAssocKey}/DefaultIcon"; ValueType= string; ValueName= ""; ValueData= "{app}/{#MyAppExeName},0"
Root = HKA; Subkey= "Software/Classes/{#MyAppAssocKey}/shell/open/command"; ValueType= string; ValueName= ""; ValueData= """{app}/{#MyAppExeName}"" ""%1"""
Root = HKA; Subkey= "Software/Classes/Applications/{#MyAppExeName}/SupportedTypes"; ValueType= string; ValueName= ".pcr"; ValueData= ""

Icons = ["Icons"]
Name= "{group}/{#MyAppName}"; Filename= "{app}/{#MyAppExeName}"
Name= "{group}/{cm:UninstallProgram,{#MyAppName}}"; Filename= "{uninstallexe}"
Name= "{autodesktop}/{#MyAppName}"; Filename= "{app}/{#MyAppExeName}"; Tasks= "desktopicon"

Run = ["Run"]
Filename= "{app}/{#MyAppExeName}"; Description= "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags= "nowait, postinstall, skipifsilent"

