import argparse
import dataclasses
from typing import Type

from rich.console import Console

from enum import StrEnum


class Mode(StrEnum):
    BLINK = "blink"
    CONSUME = "consume"
    ADD_PARTITIONS = "add_partitions"

    @classmethod
    def choices(cls) -> list[str]:
        return [v.value for v in cls.__dict__["_member_map_"].values()]


@dataclasses.dataclass
class Args:
    broker: str
    mode: Mode
    topic: set[str] | str
    interval: int
    limit: int
    group: str
    partitions: int


console = Console(color_system="truecolor", force_interactive=True)

parser = argparse.ArgumentParser(description="Kafka pythonic tool")
parser.add_argument("-b", "--broker", type=str, required=True)
parser.add_argument("-m", "--mode", choices=Mode.choices(), default="blink")
parser.add_argument("-i", "--interval", type=int, required=False, default=1)
parser.add_argument("-l", "--limit", type=int, required=False, default=None)
parser.add_argument("-t", "--topic", type=str, nargs="*", required=True)
parser.add_argument("-g", "--group", type=str, required=False)
parser.add_argument("-p", "--partitions", type=int, required=False)

args = Args(**parser.parse_args().__dict__)


def main():
    from kfk.producer import EasyProducer
    from kfk.consumer import EasyConsumer
    from kfk.client import EasyClient

    executor: Type[EasyClient | EasyProducer | EasyConsumer] = EasyClient

    match args.mode:
        case Mode.BLINK:
            executor = EasyProducer
        case Mode.CONSUME:
            executor = EasyConsumer
        case Mode.ADD_PARTITIONS:
            executor = EasyClient
    executor()


if __name__ == "__main__":
    main()
