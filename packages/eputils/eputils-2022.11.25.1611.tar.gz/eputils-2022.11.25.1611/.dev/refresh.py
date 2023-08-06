import os

print("1")
# os.system("dir")
os.system("cd python-ep-utils && py .\\.dev\\dist.py")

print("2")
os.system("cd ..")

os.system("py -m pip install --upgrade eputils")
os.system("py -m pip install --upgrade eputils") # Only picks last version after second call..?

print("3")
os.system("docker compose -f .\\docker-compose.dev.yml build --no-cache algorithm-manager")

print("4")
os.system("docker compose -f .\\local.docker-compose.build-template.yml build --no-cache")

print("Done!")
