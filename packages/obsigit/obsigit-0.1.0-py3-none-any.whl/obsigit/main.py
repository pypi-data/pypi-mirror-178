import os
import pickle
from dataclasses import dataclass, asdict, field
from dacite import from_dict
import fire

data_path = os.path.expanduser("~//.obsigit")


@dataclass
class Data:
    obsidian_vault_path:str = ""


data = Data()
if os.path.exists(data_path):
    data = from_dict(data_class=Data, data=pickle.load(open(data_path, "rb")))

def set_valut_path(path):
    data.obsidian_vault_path = path
    pickle.dump(asdict(data), open(data_path, "wb"))

def sync():
    os.chdir(data.obsidian_vault_path)
    print("git add...")
    os.system("git add *")
    print("git commit...")
    os.system("git commit -m 'nothing to say'")
    print("git pull...")
    os.system("git pull")
    print("git push...")
    os.system("git push")
    


def main():
    fire.Fire({
        "set_valut_path":set_valut_path,
        "sync":sync
    })
