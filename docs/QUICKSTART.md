# Quick Reference - Unreal Engine Python Scripts

## Setup (One Time)
```batch
cd scripts
setup.bat
```

## Activate Virtual Environment
```powershell
# PowerShell
.\venv\Scripts\Activate.ps1

# Command Prompt
venv\Scripts\activate.bat
```

## Test Configuration
```batch
python config.py
```

## Run Scripts

### Option 1: Using Batch File (Easiest)
```batch
run_python_in_unreal.bat
# or specify a script
run_python_in_unreal.bat populate_scene.py
```

### Option 2: Using Python Utility (With Virtual Env)
```batch
# Activate venv first, then:
python run_in_unreal.py
# or
python run_in_unreal.py populate_scene.py
```

### Option 3: Direct Command
```batch
"C:\Program Files\Epic Games\UE_5.6\Engine\Binaries\Win64\UnrealEditor-Cmd.exe" "C:\Users\cwood\Documents\Unreal Projects\firstperson\firstperson.uproject" -ExecutePythonScript="C:\Users\cwood\Documents\Unreal Projects\firstperson\scripts\populate_scene.py" -stdout -unattended -nosplash
```

### Option 4: From Within Unreal Editor
```python
# Python Console in Unreal:
exec(open(r'C:\Users\cwood\Documents\Unreal Projects\firstperson\scripts\populate_scene.py').read())
```

## Customize Behavior

Edit `.env` file to change:

### Project & Level Settings
- `PROJECT` - Project name (e.g., `Office`)
- `PROJECT_PATH` - Path to .uproject file
- `LEVEL` - Level name (e.g., `Main`)
- `LEVEL_PATH` - Full path to level (e.g., `/Game/Office_Pack_Vol_1/Maps/Main`)
- `AUTO_LOAD_LEVEL` - Auto-load level when running scripts (default: `true`)

Available levels:
- `main` → `/Game/Office_Pack_Vol_1/Maps/Main`
- `firstperson` → `/Game/FirstPerson/Lvl_FirstPerson`
- `horror` → `/Game/Variant_Horror/Lvl_Horror`
- `shooter` → `/Game/Variant_Shooter/Lvl_Shooter`
- `basic` → `/Game/Variant_Basic/basic_level`

### Scene Population Settings
- Grid size: `GRID_ROWS`, `GRID_COLS`, `GRID_SPACING`
- Circle pattern: `CIRCLE_OBJECTS`, `CIRCLE_RADIUS`
- Spiral pattern: `SPIRAL_OBJECTS`, `SPIRAL_MAX_RADIUS`, `SPIRAL_HEIGHT_INCREMENT`
- Random scatter: `SCATTER_OBJECTS`, `SCATTER_AREA_SIZE`

## File Structure
```
scripts/
├── .env                        # Configuration (customize this)
├── .env.example               # Template configuration
├── config.py                  # Configuration loader
├── level_utils.py            # Level/map management utilities
├── populate_scene.py          # Main demo script
├── run_in_unreal.py          # Python launcher utility
├── run_python_in_unreal.bat  # Batch launcher
├── setup.bat                 # Setup script
├── requirements.txt          # Python dependencies
├── venv/                     # Virtual environment (auto-generated)
└── README.md                 # Full documentation
```

## Troubleshooting

**"Module not found" errors:**
- Make sure virtual environment is activated
- Run: `pip install -r requirements.txt`

**Unreal Editor path not found:**
- Edit `.env` file
- Update `UNREAL_ENGINE_PATH` to your Unreal installation

**Script doesn't create objects:**
- Make sure Python Editor Script Plugin is enabled in Unreal
- Check Unreal's Output Log for Python errors

**Wrong level loads:**
- Edit `.env` file
- Update `LEVEL` (name) and `LEVEL_PATH` (full path)
- Or set `AUTO_LOAD_LEVEL=false` to use currently open level

## Quick Level Management

From within Unreal Python console:
```python
# Load level utilities
exec(open(r'C:\Users\cwood\Documents\Unreal Projects\firstperson\scripts\level_utils.py').read())

# Quick level switching
load_main()        # Office Main level
load_horror()
load_shooter()

# Or by name
load_level('main')
```
