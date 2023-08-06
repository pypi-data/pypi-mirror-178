from multiprocessing import Process, Value
import os
import pickle
import time
from dataclasses import dataclass, asdict, field
import msvcrt
from datetime import datetime, timedelta
from dacite import from_dict
import fire

data_path = os.path.expanduser("~//.bgmitimer")


@dataclass
class Data:
    work_time: list = field(default_factory=list)


data = Data()
if os.path.exists(data_path):
    data = from_dict(data_class=Data, data=pickle.load(open(data_path, "rb")))


def timer(status):
    start = datetime.now()
    i = 0
    while True:
        if not status.value:
            end = datetime.now()
            data.work_time.append((start, end))
            pickle.dump(asdict(data), open(data_path, "wb"))
            break
        min, sec = divmod(i, 60)
        print(f"{min} min{sec} sec...", end='\r')
        time.sleep(1)
        i += 1


def work():
    status = Value("i", 1)
    process = Process(target=timer, args=(status,))
    process.start()
    msvcrt.getwch()
    status.value = 0


def accumulate(time="all days"):
    totol = timedelta()
    for start, end in data.work_time:
        if time == "all days":
            dur = end - start
            totol += dur
        if time == "today":
            if start.day == datetime.now().day:
                dur = end - start
            totol += dur
    total_sec = totol.total_seconds()
    total_min, sec = divmod(total_sec, 60)
    hour, min = divmod(total_min, 60)
    print(f"{hour} hour{min} min{sec} sec...")


def main():
    fire.Fire({
        "work": work,
        "accumulate": accumulate
    })
