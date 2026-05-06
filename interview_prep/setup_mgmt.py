import os

# Create management command directories
os.makedirs("api/management/commands", exist_ok=True)

# __init__ files
open("api/management/__init__.py", "w").close()
open("api/management/commands/__init__.py", "w").close()

print("Management command scaffold created.")
