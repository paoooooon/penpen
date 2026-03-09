from enum import Enum


class TodoSubtaskUpdateStatus(str, Enum):
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    TODO = "todo"

    def __str__(self) -> str:
        return str(self.value)
