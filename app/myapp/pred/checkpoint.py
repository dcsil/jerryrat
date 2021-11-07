import json

def getCheckpoint():
    with open("./checkpoint/checkpoint.json", "r") as fp:
        checkpoint = json.load(fp)["checkpoint"]
        return checkpoint

def setCheckpoint(checkpoint=0):
    with open("./checkpoint/checkpoint.json", "r+") as fp:
        checkpoint = json.load(fp)
        checkpoint["checkpoint"] = checkpoint
        json.dump(checkpoint, fp, indent=0)
