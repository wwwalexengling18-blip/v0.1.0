;
#define MyAppName "A380 AI Crew Commander"
#define MyAppVersion "0.2.0"
#define MyPublisher "A380 AI Crew"
#define MyExe "A380_AI_Crew_Commander.exe"

[Setup]
AppId={{A2B5C10E-1D4F-4E60-9B64-1A3A0E7E5A90}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyPublisher}
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
Source: "app\{#MyExe}"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\configs\*"; DestDir: "{app}\configs"; Flags: recursesubdirs createallsubdirs ignoreversion
Source: "..\src\*"; DestDir: "{app}\src"; Flags: recursesubdirs createallsubdirs ignoreversion
Source: "..\pyproject.toml"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\INSTALL_G2G_K.cmd"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\RUN_G2G_K.cmd"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\START_ControlCenter.cmd"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyExe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyExe}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyExe}"; Description: "Commander starten"; Flags: nowait postinstall skipifsilent
