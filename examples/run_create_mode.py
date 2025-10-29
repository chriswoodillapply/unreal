"""
Run with UPSERT_MODE = False (always create new actors)
"""

# Set in globals before executing
globals()['UPSERT_MODE'] = False

with open(r'C:\Users\cwood\Documents\Unreal Projects\Office\scripts\test_upsert_config.py', 'r') as f:
    code = f.read()
    exec(code, globals())
