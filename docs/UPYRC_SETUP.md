# upyrc Setup Guide for Unreal Engine 5.6

This guide will help you set up **upyrc** (Unreal Python Remote Control) to work with Unreal Engine 5.6.

## What is upyrc?

upyrc is a Python wrapper around Unreal Engine's remote control capabilities. It provides two main modules:

1. **upyre** - Python Remote Execution (multicast UDP protocol)
   - Execute Python code in Unreal from external Python processes
   - Uses the PythonScriptPlugin's remote execution feature
   
2. **uprc** - HTTP Remote Control API
   - Control Unreal via HTTP REST API
   - Get/Set properties, call functions, query objects
   - Uses the WebRemoteControl plugin

## Prerequisites

- Unreal Engine 5.6 installed
- Python 3.7 or higher
- Project: `firstperson.uproject`

## Step 1: Install Python Package

The required changes have already been made to your project. Just install the Python package:

```powershell
cd "c:\Users\cwood\Documents\Unreal Projects\firstperson\scripts"
pip install -r requirements.txt
```

This will install:
- `upyrc` - Unreal Python Remote Control wrapper
- `python-dotenv` - Configuration management

## Step 2: Project Configuration (Already Done!)

The following changes have already been applied to your project:

### ✅ Plugins Enabled in `firstperson.uproject`

- **PythonScriptPlugin** - Enables Python scripting
- **WebRemoteControl** - Enables HTTP remote control API

### ✅ Python Plugin Settings in `Config/DefaultEngine.ini`

```ini
[/Script/PythonScriptPlugin.PythonScriptPluginSettings]
bRemoteExecution=True
RemoteExecutionMulticastGroupEndpoint=239.0.0.1:6766
RemoteExecutionMulticastBindAddress=0.0.0.0
RemoteExecutionSendBufferSizeBytes=2097152
RemoteExecutionReceiveBufferSizeBytes=2097152
bRemoteExecutionMulticastAutoConnectionEnabled=True
```

### ✅ WebRemoteControl Settings in `Config/DefaultEngine.ini`

```ini
[/Script/WebRemoteControl.WebRemoteControlSettings]
bServerStartByDefault=True
RemoteControlHttpServerPort=30010
RemoteControlWebInterfacePort=7000
bWebAppEnabled=True
```

## Step 3: Open Unreal Editor

1. **Open your project** in Unreal Editor:
   ```
   firstperson.uproject
   ```

2. The first time you open the project after enabling the plugins, you'll see:
   - "New plugins are available" dialog
   - **Click "Yes"** to rebuild the project modules
   - This may take a few minutes

3. After the editor opens, verify plugins are loaded:
   - Go to **Edit → Plugins**
   - Search for "Python" - should show **Python Editor Script Plugin** as ENABLED
   - Search for "Remote" - should show **Web Remote Control** as ENABLED

## Step 4: Start Remote Control Server

In Unreal Editor, open the **Output Log** (Window → Developer Tools → Output Log).

Run these console commands:

```
WebControl.StartServer
WebControl.EnableServerOnStartup
```

You should see output like:
```
LogWebControl: Web Remote Control server started on port 30010
```

**Optional:** To automatically start the server on launch, the setting `bServerStartByDefault=True` is already configured.

## Step 5: Test the Setup

Run the test script:

```powershell
cd "c:\Users\cwood\Documents\Unreal Projects\firstperson\scripts"
python test_upyrc.py
```

This will test:
1. **upyre** - Python remote execution via UDP multicast
2. **uprc** - HTTP Remote Control API

Expected output:
```
✓ upyre tests PASSED!
✓ uprc tests PASSED!
🎉 All tests passed! upyrc is working correctly with Unreal 5.6
```

## Usage Examples

### Example 1: Execute Python Code Remotely (upyre)

```python
from upyrc import upyre

# Create config from project file
config = upyre.RemoteExecutionConfig.from_uproject_path(
    r"c:\Users\cwood\Documents\Unreal Projects\firstperson\firstperson.uproject"
)

# Connect and execute
with upyre.PythonRemoteConnection(config) as conn:
    # Simple statement
    result = conn.execute_python_command(
        "import unreal; unreal.log('Hello from Python!')",
        exec_type=upyre.ExecTypes.EXECUTE_STATEMENT
    )
    
    # Execute a file
    result = conn.execute_python_command(
        "path/to/script.py",
        exec_type=upyre.ExecTypes.EXECUTE_FILE
    )
```

### Example 2: Use HTTP Remote Control (uprc)

```python
from upyrc import uprc

# Connect to Unreal
conn = uprc.URConnection(host="127.0.0.1", port=30010)

# Get editor subsystems
actor_subsystem = conn.get_editor_actor_subsystem()
asset_library = conn.get_editor_asset_library()

# Get object by path
obj = conn.get_uobject("/Game/MyBlueprint")

# Call function
result = obj.call_function("MyFunction", {"param": "value"})

# Get/Set properties
value = obj.get_property("MyProperty")
obj.set_property("MyProperty", new_value)
```

### Example 3: Use Existing Scripts

You already have a `upyrc_send.py` script. Use it like this:

```powershell
# Execute a Python file in Unreal
python upyrc_send.py quick_test.py

# Execute code directly
python upyrc_send.py -c "import unreal; unreal.log('Test')"
```

## Troubleshooting

### Issue: "upyrc not installed"
**Solution:** Run `pip install upyrc`

### Issue: "Could not connect to Unreal"
**Solution:** 
1. Make sure Unreal Editor is running
2. Make sure the project is loaded (not just the launcher)
3. Check the Output Log for Python plugin errors

### Issue: "Remote Control API not responding"
**Solution:**
1. Run console command: `WebControl.StartServer`
2. Check port 30010 is not blocked by firewall
3. Verify WebRemoteControl plugin is enabled

### Issue: "Python remote execution failed"
**Solution:**
1. Check Python plugin is enabled: Edit → Plugins → Python Editor Script Plugin
2. Verify settings in DefaultEngine.ini (already configured)
3. Check Windows Firewall allows UDP multicast on port 6766

### Issue: "Module rebuild required"
**Solution:**
1. Close Unreal Editor
2. Delete `Binaries`, `Intermediate`, `Saved` folders (except `Saved/Config`)
3. Right-click `firstperson.uproject` → **Generate Visual Studio project files**
4. Open the `.uproject` file again

## Network Configuration

The default settings should work for local development:

- **Python Remote Execution (upyre)**
  - Protocol: UDP Multicast
  - Multicast Group: 239.0.0.1:6766
  - Bind Address: 0.0.0.0

- **HTTP Remote Control (uprc)**
  - Protocol: HTTP REST API
  - Host: 127.0.0.1 (localhost)
  - Port: 30010

For remote connections (different machines), update:
1. Change `RemoteExecutionMulticastBindAddress` to your network interface IP
2. Change `uprc` connection host to Unreal machine's IP
3. Configure firewall rules for ports 6766 (UDP) and 30010 (TCP)

## Additional Resources

- **upyrc Documentation:** https://github.com/cgtoolbox/UnrealRemoteControlWrapper/wiki
- **PyPI Package:** https://pypi.org/project/upyrc/
- **Test Project:** https://github.com/cgtoolbox/UnrealRemoteControlTestData
- **UE Remote Control API Docs:** https://docs.unrealengine.com/5.6/en-US/remote-control-api-in-unreal-engine/

## Quick Reference

### Console Commands (in Unreal Editor)

```
# Start/stop remote control server
WebControl.StartServer
WebControl.StopServer
WebControl.EnableServerOnStartup
WebControl.DisableServerOnStartup

# Check Python plugin status
py import unreal; print(unreal.SystemLibrary.get_engine_version())
```

### Python Scripts (external)

```powershell
# Test connection
python test_upyrc.py

# Send code via upyre
python upyrc_send.py -c "import unreal; unreal.log('Hello')"

# Execute script file
python upyrc_send.py populate_scene.py
```

## Configuration Files Modified

✅ `firstperson.uproject` - Added PythonScriptPlugin and WebRemoteControl
✅ `Config/DefaultEngine.ini` - Added plugin settings
✅ `scripts/requirements.txt` - Added upyrc package
✅ Created `test_upyrc.py` - Comprehensive test script
✅ Created this guide: `UPYRC_SETUP.md`

---

**Ready to use!** Your Unreal Engine 5.6 project is now configured for upyrc. 🚀
