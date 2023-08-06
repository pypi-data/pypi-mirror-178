from typing import Mapping, Any


class CreateEvent:  # 创建迭代
    def __init__(self, sprit_id: str = "", title: str = "", start_time: int = 0, end_time: int = 0, **param):
        self.sprit_id = sprit_id
        self.title = title
        self.start_time = start_time
        self.end_time = end_time


class UpdateEvent:  # 更新迭代
    def __init__(self, sprit_id: str = "", old_title: str = "", new_title: str = "",
                 old_start_time: int = 0, new_start_time: int = 0, old_end_time: int = 0,
                 new_end_time: int = 0, **param):
        self.sprit_id = sprit_id
        self.old_title = old_title
        self.new_title = new_title
        self.old_start_time = old_start_time
        self.new_start_time = new_start_time
        self.old_end_time = old_end_time
        self.new_end_time = new_end_time


class RemoveEvent:  # 删除迭代
    def __init__(self, sprit_id: str = "", title: str = "", start_time: int = 0, end_time: int = 0, **param):
        self.sprit_id = sprit_id
        self.title = title
        self.start_time = start_time
        self.end_time = end_time


SpritEvents = CreateEvent | UpdateEvent | RemoveEvent | None


def parseSpritEvent(ev: Mapping[str, Mapping[str, Any]]) -> SpritEvents:
    if "CreateEvent" in ev:
        return CreateEvent(**ev["CreateEvent"])
    elif "UpdateEvent" in ev:
        return UpdateEvent(**ev["UpdateEvent"])
    elif "RemoveEvent" in ev:
        return UpdateEvent(**ev["RemoveEvent"])
    else:
        return None
