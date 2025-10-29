"""
Run with UPSERT_MODE = True (update existing actors)
"""

# Set in globals before executing
globals()['UPSERT_MODE'] = True

with open(r'C:\Users\cwood\Documents\Unreal Projects\Office\scripts\test_upsert_config.py', 'r') as f:
    code = f.read()
    exec(code, globals())
