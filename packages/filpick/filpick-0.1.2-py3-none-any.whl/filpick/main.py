import os
import pickle
from dataclasses import dataclass, asdict, field
from dacite import from_dict
import fire

data_path = os.path.expanduser("~//.filpick")


@dataclass
class Data:
    root_path: str = ""
    results: list = field(default_factory=list)


data = Data()
if os.path.exists(data_path):
    data = from_dict(data_class=Data, data=pickle.load(open(data_path, "rb")))


def set_root_path(path):
    data.root_path = path
    pickle.dump(asdict(data), open(data_path, "wb"))


def list():
    data.results = os.listdir(data.root_path)
    for i, file_name in enumerate(data.results):
        print(str(i)+" -> "+file_name)
    pickle.dump(asdict(data), open(data_path, "wb"))


def open_(index):
    file_name = data.results[index]
    os.chdir(data.root_path)
    os.system(f'"{file_name}"')


def main():
    fire.Fire({
        "set_root_path": set_root_path,
        "list": list,
        "open": open_
    })
