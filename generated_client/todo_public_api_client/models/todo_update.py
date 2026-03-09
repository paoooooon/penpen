from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.todo_update_priority import TodoUpdatePriority
from ..models.todo_update_status import TodoUpdateStatus
from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
import datetime






T = TypeVar("T", bound="TodoUpdate")



@_attrs_define
class TodoUpdate:
    """ TODO更新リクエスト

        Attributes:
            project_id (int | None | Unset): プロジェクトID Example: 1.
            worker_id (int | Unset): 作業者ID Example: 1.
            agent_id (int | None | Unset): エージェントID Example: 1.
            title (str | Unset): TODOタイトル Example: サンプルTODO.
            description (None | str | Unset): TODOの説明 Example: これはサンプルTODOです.
            status (TodoUpdateStatus | Unset): ステータス Example: in_progress.
            priority (TodoUpdatePriority | Unset): 優先度 Example: high.
            due_date (datetime.datetime | None | Unset): 期限日時 Example: 2024-12-31T23:59:59Z.
     """

    project_id: int | None | Unset = UNSET
    worker_id: int | Unset = UNSET
    agent_id: int | None | Unset = UNSET
    title: str | Unset = UNSET
    description: None | str | Unset = UNSET
    status: TodoUpdateStatus | Unset = UNSET
    priority: TodoUpdatePriority | Unset = UNSET
    due_date: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        project_id: int | None | Unset
        if isinstance(self.project_id, Unset):
            project_id = UNSET
        else:
            project_id = self.project_id

        worker_id = self.worker_id

        agent_id: int | None | Unset
        if isinstance(self.agent_id, Unset):
            agent_id = UNSET
        else:
            agent_id = self.agent_id

        title = self.title

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        status: str | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value


        priority: str | Unset = UNSET
        if not isinstance(self.priority, Unset):
            priority = self.priority.value


        due_date: None | str | Unset
        if isinstance(self.due_date, Unset):
            due_date = UNSET
        elif isinstance(self.due_date, datetime.datetime):
            due_date = self.due_date.isoformat()
        else:
            due_date = self.due_date


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if worker_id is not UNSET:
            field_dict["worker_id"] = worker_id
        if agent_id is not UNSET:
            field_dict["agent_id"] = agent_id
        if title is not UNSET:
            field_dict["title"] = title
        if description is not UNSET:
            field_dict["description"] = description
        if status is not UNSET:
            field_dict["status"] = status
        if priority is not UNSET:
            field_dict["priority"] = priority
        if due_date is not UNSET:
            field_dict["due_date"] = due_date

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        def _parse_project_id(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        project_id = _parse_project_id(d.pop("project_id", UNSET))


        worker_id = d.pop("worker_id", UNSET)

        def _parse_agent_id(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        agent_id = _parse_agent_id(d.pop("agent_id", UNSET))


        title = d.pop("title", UNSET)

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))


        _status = d.pop("status", UNSET)
        status: TodoUpdateStatus | Unset
        if isinstance(_status,  Unset):
            status = UNSET
        else:
            status = TodoUpdateStatus(_status)




        _priority = d.pop("priority", UNSET)
        priority: TodoUpdatePriority | Unset
        if isinstance(_priority,  Unset):
            priority = UNSET
        else:
            priority = TodoUpdatePriority(_priority)




        def _parse_due_date(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                due_date_type_0 = isoparse(data)



                return due_date_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        due_date = _parse_due_date(d.pop("due_date", UNSET))


        todo_update = cls(
            project_id=project_id,
            worker_id=worker_id,
            agent_id=agent_id,
            title=title,
            description=description,
            status=status,
            priority=priority,
            due_date=due_date,
        )


        todo_update.additional_properties = d
        return todo_update

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
