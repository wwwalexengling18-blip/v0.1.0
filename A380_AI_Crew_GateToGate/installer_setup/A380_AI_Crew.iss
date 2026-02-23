;
; A380 AI Crew – Modern Setup.exe (Inno Setup 6)
#define MyAppName "A380 AI Crew (Gate-to-Gate)"
#define MyAppVersion "0.1.0"
#define MyAppPublisher "A380 AI Crew"
#define MyAppExeName "A380_AI_Crew_ControlCenter.exe"

[Setup]
AppId={{2A5C5F0B-0F3E-4E62-A1C6-0D0DAD40A7F2}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={userdocs}\FBW_A380_Tools\A380_AI_Crew_GateToGate
DisableProgramGroupPage=yes
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
OutputBaseFilename=Setup_{#MyAppName}_{#MyAppVersion}

[Languages]
Name: "german"; MessagesFile: "compiler:Languages\German.isl"

[Tasks]
Name: "desktopicon"; Description: "Desktop-Verknüpfung erstellen"; GroupDescription: "Verknüpfungen:"

[Files]
; App EXE (wird vom Build in installer_setup\app\ gelegt)
Source: "app\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

; Projektdateien (Plan, src, profiles, tools) als Payload
Source: "..\src\*"; DestDir: "{app}\src"; Flags: recursesubdirs createallsubdirs ignoreversion
Source: "..\pyproject.toml"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\INSTALL_G2G_K.cmd"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\RUN_G2G_K.cmd"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\START_G2G_K.cmd"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Control Center starten"; Flags: nowait postinstall skipifsilent
