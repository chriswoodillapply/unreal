# Quick Start: upyrc with Unreal 5.6

## 🚀 Installation (3 Steps)

### 1. Install Python Package
```powershell
cd "c:\Users\cwood\Documents\Unreal Projects\firstperson\scripts"
.\setup_upyrc.bat
```

Or manually:
```powershell
pip install -r requirements.txt
```

### 2. Open Unreal Editor
- Open `firstperson.uproject`
- Click **Yes** if prompted to rebuild plugins
- Wait for editor to load

### 3. Start Remote Control Server
In Unreal's **Output Log** window, run:
```
WebControl.StartServer
```

## ✅ Test It Works
```powershell
python test_upyrc.py
```

Expected: `✓ All tests passed! upyrc is working correctly with Unreal 5.6`

## 📝 Usage Examples

### Send Python Code to Unreal
```powershell
# Execute a script file
python upyrc_send.py populate_scene.py

# Run code directly
python upyrc_send.py -c "import unreal; unreal.log('Hello World!')"
```

### Use in Your Python Scripts

**upyre** (Execute Python in Unreal):
```python
from upyrc import upyre

config = upyre.RemoteExecutionConfig.from_uproject_path(
    r"c:\Users\cwood\Documents\Unreal Projects\firstperson\firstperson.uproject"
)

with upyre.PythonRemoteConnection(config) as conn:
    result = conn.execute_python_command(
        "import unreal; unreal.log('Hello!')",
        exec_type=upyre.ExecTypes.EXECUTE_STATEMENT
    )
```

**uprc** (HTTP API):
```python
from upyrc import uprc

conn = uprc.URConnection(host="127.0.0.1", port=30010)
actor_subsystem = conn.get_editor_actor_subsystem()
asset_lib = conn.get_editor_asset_library()
```

## 📚 Full Documentation
See `UPYRC_SETUP.md` for complete setup guide and troubleshooting.

## ⚙️ What Was Configured

✅ Enabled plugins:
  - PythonScriptPlugin
  - WebRemoteControl

✅ Configured settings:
  - Python remote execution: UDP multicast on 239.0.0.1:6766
  - Web remote control: HTTP server on localhost:30010

✅ Created scripts:
  - `test_upyrc.py` - Test both upyre and uprc
  - `upyrc_send.py` - Send Python code to Unreal
  - `setup_upyrc.bat` - Automated setup

---
🎯 **Ready to use!** Control Unreal 5.6 from external Python scripts.
