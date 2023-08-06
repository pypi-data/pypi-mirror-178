import time

from kafka import KafkaProducer

from kfk.main import console, args


class EasyProducer:
    def __init__(
        self,
    ):
        self.client = KafkaProducer(bootstrap_servers=args.broker)

        try:
            match args.mode:
                case "blink":
                    self.blink(args.topic[0])
        except KeyboardInterrupt:
            console.print("[bold red]Closed.[/bold red]")

    def blink(self, topic: str):
        counter = 1
        condition = counter < args.limit if args.limit else True
        with console.status("Producing messages...", spinner="aesthetic") as status:
            while condition:
                message = f"Message #{counter}"
                self.client.send(topic, value=message.encode("utf-8"))
                console.log(f"Message delivered! Content: {message}")

                counter += 1
                time.sleep(args.interval)
                condition = counter < args.limit if args.limit else True
