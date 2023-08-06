class Service:
    def __init__(self, name: str, url: str, branches: list):
        self.name = name
        self.url = url
        self.branches = branches

    @classmethod
    def from_dict(cls, name: str, data: dict):
        branches = [Branch.from_dict(b) for b in data["branches"]]
        return cls(name, data["url"], branches)


class Branch:
    def __init__(self, name: str, _from: str = None, args: list = []):
        self.name = name
        self.base = _from
        self.args = args

    @classmethod
    def from_dict(cls, data: dict):
        _from = data["from"] if "from" in data else None
        args = data["args"] if "args" in data else []
        return cls(data["name"], _from, args)

