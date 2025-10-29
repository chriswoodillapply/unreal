"""
Monitor UE Output Log for remote execution messages
Run this while testing to see what's happening
"""
import time
import sys

print("\n" + "="*60)
print("  WAITING FOR REMOTE EXECUTION SERVER...")
print("="*60)
print("\nInstructions:")
print("1. Make sure this script is running")
print("2. In UE: Edit → Project Settings → Python - Remote Execution")
print("3. Enable Remote Execution (check the box)")
print("4. Watch this window for confirmation\n")
print("Monitoring for server startup...\n")

# Simulate monitoring (in reality, you'd need to tail the log file)
# UE log is typically at: Saved/Logs/Office.log

import os
from pathlib import Path

log_path = Path(r"C:\Users\cwood\Documents\Unreal Projects\Office\Saved\Logs")

if log_path.exists():
    # Find most recent log file
    log_files = list(log_path.glob("*.log"))
    if log_files:
        latest_log = max(log_files, key=lambda p: p.stat().st_mtime)
        print(f"📄 Monitoring: {latest_log.name}\n")
        
        # Get current size
        last_size = latest_log.stat().st_size
        
        print("👀 Watching for new log entries...")
        print("   (Enable Remote Execution in UE now)\n")
        
        try:
            while True:
                time.sleep(0.5)
                current_size = latest_log.stat().st_size
                
                if current_size > last_size:
                    # Read new content
                    with open(latest_log, 'r', encoding='utf-8', errors='ignore') as f:
                        f.seek(last_size)
                        new_content = f.read()
                        
                        # Check for remote execution messages
                        for line in new_content.split('\n'):
                            if 'Remote' in line or 'Python' in line or 'remote' in line:
                                if 'execution server started' in line.lower():
                                    print(f"\n✅ {line.strip()}\n")
                                    print("🎉 SUCCESS! Server is running!")
                                    print("\nNow run: python test_direct_udp.py\n")
                                    sys.exit(0)
                                elif 'failed' in line.lower() or 'error' in line.lower():
                                    print(f"\n❌ {line.strip()}\n")
                                else:
                                    print(f"   {line.strip()}")
                    
                    last_size = current_size
                    
        except KeyboardInterrupt:
            print("\n\nMonitoring stopped.")
    else:
        print("❌ No log files found")
        print("   UE might not be running")
else:
    print("❌ Log directory not found:")
    print(f"   {log_path}")
    print("\n   Make sure Office project is running in UE")
