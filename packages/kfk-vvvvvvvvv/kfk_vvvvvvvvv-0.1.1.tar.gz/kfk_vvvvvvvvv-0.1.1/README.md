# KFK
## Install
```bash
pip install -i https://test.pypi.org/simple/ kfk-vvvvvvvvv
```
## Parameters:
### Required
`-b <str>` - Broker address `host:port` \
`-m [blink consume add_partitions]` - Operation to execute \
`-t [<str>]` - Topics list \

### Optional
`-i <int>` - Interval between messages in seconds. **default** = `1` \
`-l <int>` - Limit number of messages to send. **default** = `None` (unlimited) \
`-g <str>` - Consumer group name. **default** = `None`\
`-p <int>` - Increase partition number for topic. **required** for `add_partitions` mode

### Blink
Send messages like `Message #n`, where `n` - message order from 1 to value of `-l` parameter
```bash
kfk -b localhost:9092 -m blink -t myTopic

[15:08:45] Message delivered! Content: Message #1                                                                                                                                                                                        producer.py:28
[15:08:46] Message delivered! Content: Message #2                                                                                                                                                                                        producer.py:28
[15:08:47] Message delivered! Content: Message #3                                                                                                                                                                                        producer.py:28
[15:08:48] Message delivered! Content: Message #4 
```

### Consume
```bash
kfk -b localhost:9092 -m consume -t myGroup -g myGroup
```

### Add partitions
```bash
kfk -b localhost:9092 -m add_partitions -t myTopic -p 10

Trying to increase partitions from 1 -> 10
Successfully changed to 1
```