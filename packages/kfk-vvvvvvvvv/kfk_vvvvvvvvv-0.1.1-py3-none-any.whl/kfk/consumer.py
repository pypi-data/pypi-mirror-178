from datetime import datetime

from kafka import KafkaConsumer
from rich.text import Text

from kfk.main import console, args


class EasyConsumer:
    def __init__(
        self,
    ):
        self.client = KafkaConsumer(
            *args.topic, bootstrap_servers=args.broker, group_id=args.group, auto_offset_reset="latest"
        )

        try:
            match args.mode:
                case "consume":
                    self.consume()
        except KeyboardInterrupt:
            console.print("[bold red]Closed.[/bold red]")

    def consume(self):
        with console.status(
            f"Consuming messages from [bold green]{args.topic}[/bold green] topics...", spinner="aesthetic"
        ) as status:
            for msg in self.client:
                dt = Text()
                console.print(
                    f"[blue]{datetime.now().strftime('%H:%M:%S')}[blue]",
                    f"[[bold red]{msg.topic}[/bold red]: [bold yellow]{msg.offset}[/bold yellow]]",
                    msg.key if msg.key else "",
                    msg.value.decode("utf-8"),
                    dt,
                )
