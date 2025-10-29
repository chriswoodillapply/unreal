# Remote Execution Testing Checklist

## 1️⃣ Verify Config Files

### DefaultEngine.ini
Location: `C:\Users\cwood\Documents\Unreal Projects\Office\Config\DefaultEngine.ini`

Should contain:
```ini
[/Script/PythonScriptPlugin.PythonScriptPluginSettings]
bRemoteExecution=True
RemoteExecutionMulticastGroupEndpoint=127.0.0.1:6766
RemoteExecutionMulticastBindAddress=0.0.0.0

[/Script/RemoteControl.RemoteControlSettings]
bEnableRemoteExecution=True
bAllowPythonExecution=True
```

✅ **Status**: FIXED (switched to localhost 127.0.0.1)

---

## 2️⃣ Verify UE Project Settings (GUI)

**In Unreal Editor:**
1. Edit → Project Settings
2. Navigate to: **Plugins → Python - Remote Execution**
3. Check: **✓ Enable Remote Execution** = ON
4. Verify fields:
   - Multicast Group Endpoint: `127.0.0.1:6766`
   - Bind Address: `0.0.0.0`
   - Send Buffer Size: (default)

5. Navigate to: **Plugins → Remote Control**
6. Check: **✓ Enable Remote Execution** = ON
7. Check: **✓ Allow Python Execution** = ON

**⚠️ RESTART UE** after any changes!

---

## 3️⃣ Check UE Output Log

**After UE starts, look for:**
```
LogPythonRemoteExecution: Remote execution server started, listening on 127.0.0.1:6766
```

❌ **If missing** → Config not applied or firewall blocking
✅ **If present** → Server is ready!

---

## 4️⃣ Firewall Check

**Windows Firewall:**
- Allow `UnrealEditor.exe` on both Private and Public networks
- Path: `C:\Program Files\Epic Games\UE_5.6\Engine\Binaries\Win64\UnrealEditor.exe`

**Quick test:**
```powershell
# Temporarily disable to test (re-enable after!)
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False
```

---

## 5️⃣ Test with Epic's Official Client

**Run from scripts folder:**
```powershell
cd "C:\Users\cwood\Documents\Unreal Projects\firstperson\scripts"
.\venv\Scripts\activate
python test_epic_client.py
```

**Expected output:**
```
🔌 Testing connection to Unreal Engine...
✓ Connected: True

📝 Test 1: Sending log message...
   → Check UE Output Log for '🎯 REMOTE PYTHON OK!'

📝 Test 2: Getting Unreal version...
   Engine Version: 5.6.1-...

📝 Test 3: Spawning test cube...
   → Check UE viewport for cube at origin!

✅ All tests complete!
```

---

## 6️⃣ If Epic Client Works → Test Our Client

**Update send_to_unreal.py** to use localhost:
```python
UNREAL_HOST = '127.0.0.1'  # Changed from multicast
UNREAL_PORT = 6766
```

**Run diagnostic:**
```powershell
python send_to_unreal.py diagnostic_test.py
```

---

## 7️⃣ Troubleshooting Matrix

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| No "server started" log | Config not applied | Restart UE, check Project Settings GUI |
| Epic client can't connect | Firewall/port blocked | Allow UnrealEditor.exe in firewall |
| Our client fails, Epic works | Protocol mismatch | Use Epic's remote_execution module |
| Logs appear, no spawn | Wrong world context | Use `unreal.run_on_game_thread()` |
| Multicast issues | NIC/VPN blocking | Use 127.0.0.1 (loopback) |

---

## ✅ Success Criteria

- [ ] "Remote execution server started" in UE Output Log
- [ ] Epic's test client connects and logs "🎯 REMOTE PYTHON OK!"
- [ ] Test cube spawns at origin (visible in viewport)
- [ ] Our client can execute diagnostic_test.py
- [ ] populate_scene.py spawns 5x5 grid via remote execution

---

## 🔧 Current Status

**Last Updated**: Just now
**Config**: Fixed (localhost, Remote Control added)
**Next Step**: User must restart UE and run test_epic_client.py
