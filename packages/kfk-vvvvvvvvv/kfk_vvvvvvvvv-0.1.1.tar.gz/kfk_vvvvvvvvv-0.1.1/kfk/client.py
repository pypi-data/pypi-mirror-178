from kafka.admin import NewPartitions
from kafka.errors import InvalidPartitionsError
from kafka import KafkaAdminClient

from kfk.main import console, args, Mode


class EasyClient:
    def __init__(
        self,
    ):
        self.client = KafkaAdminClient(bootstrap_servers=args.broker)
        args.topic = args.topic[0]
        try:
            match args.mode:
                case Mode.ADD_PARTITIONS.value:
                    self.add_partitions()
        except KeyboardInterrupt:
            console.print("[bold red]Closed.[/bold red]")
        finally:

            self.client.close()

    def add_partitions(self):
        try:

            def partitions_initial_n():
                return len(self.client.describe_topics(args.topic)[0]["partitions"])

            console.print(
                f"[yellow]Trying to increase partitions from {partitions_initial_n()} -> {args.partitions}[yellow]"
            )

            self.client.create_partitions({args.topic: NewPartitions(args.partitions)})

            console.print(f"Successfully changed to {partitions_initial_n()}")

        except InvalidPartitionsError as e:
            console.print(
                f"[bold red]Invalid number of partitions: [bold white]{args.partitions}[/bold white]![/bold red]"
            )
            exit(1)
