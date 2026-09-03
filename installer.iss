#define AppName "RAEV Shield"
#define AppVersion "0.1.0"
#define AppPublisher "Rafael G.G."
#define AppExeName "RAEV-Shield.exe"

[Setup]
AppId={{D942587D-E51B-46DE-BD18-B3777E7D45E7}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
DefaultDirName={autopf}\RAEV Shield
DefaultGroupName=RAEV Shield
OutputDir=installer-output
OutputBaseFilename=RAEV-Shield-Setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
UninstallDisplayName=RAEV Shield

[Files]
Source: "dist\{#AppExeName}"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\RAEV Shield"; Filename: "{app}\{#AppExeName}"
Name: "{autodesktop}\RAEV Shield"; Filename: "{app}\{#AppExeName}"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Crear acceso directo en el escritorio"; GroupDescription: "Accesos directos:"; Flags: unchecked

[Run]
Filename: "{app}\{#AppExeName}"; Description: "Abrir RAEV Shield"; Flags: nowait postinstall skipifsilent
