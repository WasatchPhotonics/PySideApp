; See the file py2exe_applicatin.py for details on how to create a
; windows installer
;
; Redefine these for the application to be built
#define MyAppName "PySideApp"
#define module_name "pysideapp"
#define MyAppExeName "PySideApp.exe"
;
;
; Built for InnoSetup version 5.5.6 on Windows 7 x64
;
;
; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

; Auto Versioning section
; Read the previous build number. If there is none take 0
#define BuildNum Int(ReadIni(SourcePath + "\\BuildInfo.ini","Info","Build","0"))

; Increment the build number by one
#expr BuildNum = BuildNum + 1

; Store the number in the ini file for the next build.
#expr WriteIni(SourcePath + "\\BuildInfo.ini","Info","Build",BuildNum)


#define MyAppPublisher "Wasatch Photonics"
#define MyAppURL "http://wasatchphotonics.com"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{B9977C21-3BA0-4CCB-8398-0B78F34DC849}

; See auto versioning section above
; Make the major version bumps manual here and have the command line
; builds part of the auto-increment
AppVersion=0.1.{#BuildNum}

AppName={#MyAppName}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={pf}\{#MyAppName}
DisableDirPage=yes
DefaultGroupName={#MyAppName}
OutputDir=windows_installer
OutputBaseFilename={#MyAppName}_setup
Compression=lzma
SolidCompression=yes
SetupIconFile=..\{#module_name}\assets\images\ApplicationIcon.ico
UninstallDisplayIcon={app}\{#MyAppName}\{#MyAppExeName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "built-dist\*"; DestDir: "{app}"; Flags: recursesubdirs ignoreversion

; There are many ways to include a Visual Studio runtime distributable. This way is to copy the dll into the application folder.
Source: "support_files\msvcr100.dll"; DestDir: "{app}\{#MyAppName}\"; Flags: recursesubdirs ignoreversion


; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppName}\{#MyAppExeName}"; IconFilename: "{app}\{#MyAppName}\{#MyAppExeName}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppName}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppName}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
