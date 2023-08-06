import os
import pickle
from dataclasses import dataclass, asdict
from dacite import from_dict
import fire

data_path = os.path.expanduser("~//.obsigit")


@dataclass
class Data:
    obsidian_vault_path: str = ""
    commit_message: str = "nothing to say"


data = Data()
if os.path.exists(data_path):
    data = from_dict(data_class=Data, data=pickle.load(open(data_path, "rb")))


def set_valut_path(path):
    data.obsidian_vault_path = path
    pickle.dump(asdict(data), open(data_path, "wb"))


def set_commit_message(message):
    data.commit_message = message
    pickle.dump(asdict(data), open(data_path, "wb"))


def sync():
    os.chdir(data.obsidian_vault_path)
    print("git add...")
    os.system("git add *")
    print("git commit...")
    os.system(f'git commit -m "{data.commit_message}"')
    print("git pull...")
    os.system("git pull")
    print("git push...")
    os.system("git push")


def main():
    fire.Fire({
        "set_valut_path": set_valut_path,
        "set_commit_message": set_commit_message,
        "sync": sync
    })
