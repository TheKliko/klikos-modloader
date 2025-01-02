from datetime import datetime, timezone


class Entry:
    timestamp: float
    prefixes: list[str] = []
    original: str
    message: str
    level: str | None = None


    def __init__(self, data: str):
        self.original = data
        self.timestamp = datetime.strptime(data.split(",")[0], "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc).timestamp()

        split_data: list[str] = data.split()[1:]
        for item in split_data:
            if item.startswith("[") and item.endswith("]"):
                self.prefixes.append(item)
            else:
                break

        self.message = " ".join(data.split()[1+len(self.prefixes):])
        
        level = item.split()[0].split(",")[-1]
        try:
            int(level)
        except ValueError:
            self.level = level