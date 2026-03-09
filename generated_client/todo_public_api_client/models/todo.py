from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.todo_priority import TodoPriority
from ..models.todo_status import TodoStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="Todo")


@_attrs_define
class Todo:
    """TODO情報

    Attributes:
        id (int): TODO ID Example: 1.
        worker_id (int): 作業者ID Example: 1.
        title (str): TODOタイトル Example: サンプルTODO.
        status (TodoStatus): ステータス Example: todo.
        priority (TodoPriority): 優先度 Example: medium.
        created_at (datetime.datetime): 作成日時 Example: 2024-01-01T00:00:00Z.
        updated_at (datetime.datetime): 更新日時 Example: 2024-01-01T00:00:00Z.
        uuid (None | Unset | UUID): UUID Example: 550e8400-e29b-41d4-a716-446655440000.
        project_id (int | None | Unset): プロジェクトID Example: 1.
        agent_id (int | None | Unset): エージェントID Example: 1.
        description (None | str | Unset): TODOの説明 Example: これはサンプルTODOです.
        due_date (datetime.datetime | None | Unset): 期限日時 Example: 2024-12-31T23:59:59Z.
        completed_at (datetime.datetime | None | Unset): 完了日時
    """

    id: int
    worker_id: int
    title: str
    status: TodoStatus
    priority: TodoPriority
    created_at: datetime.datetime
    updated_at: datetime.datetime
    uuid: None | Unset | UUID = UNSET
    project_id: int | None | Unset = UNSET
    agent_id: int | None | Unset = UNSET
    description: None | str | Unset = UNSET
    due_date: datetime.datetime | None | Unset = UNSET
    completed_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        worker_id = self.worker_id

        title = self.title

        status = self.status.value

        priority = self.priority.value

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        uuid: None | str | Unset
        if isinstance(self.uuid, Unset):
            uuid = UNSET
        elif isinstance(self.uuid, UUID):
            uuid = str(self.uuid)
        else:
            uuid = self.uuid

        project_id: int | None | Unset
        if isinstance(self.project_id, Unset):
            project_id = UNSET
        else:
            project_id = self.project_id

        agent_id: int | None | Unset
        if isinstance(self.agent_id, Unset):
            agent_id = UNSET
        else:
            agent_id = self.agent_id

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        due_date: None | str | Unset
        if isinstance(self.due_date, Unset):
            due_date = UNSET
        elif isinstance(self.due_date, datetime.datetime):
            due_date = self.due_date.isoformat()
        else:
            due_date = self.due_date

        completed_at: None | str | Unset
        if isinstance(self.completed_at, Unset):
            completed_at = UNSET
        elif isinstance(self.completed_at, datetime.datetime):
            completed_at = self.completed_at.isoformat()
        else:
            completed_at = self.completed_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "worker_id": worker_id,
                "title": title,
                "status": status,
                "priority": priority,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if agent_id is not UNSET:
            field_dict["agent_id"] = agent_id
        if description is not UNSET:
            field_dict["description"] = description
        if due_date is not UNSET:
            field_dict["due_date"] = due_date
        if completed_at is not UNSET:
            field_dict["completed_at"] = completed_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        worker_id = d.pop("worker_id")

        title = d.pop("title")

        status = TodoStatus(d.pop("status"))

        priority = TodoPriority(d.pop("priority"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        def _parse_uuid(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                uuid_type_0 = UUID(data)

                return uuid_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        uuid = _parse_uuid(d.pop("uuid", UNSET))

        def _parse_project_id(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        project_id = _parse_project_id(d.pop("project_id", UNSET))

        def _parse_agent_id(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        agent_id = _parse_agent_id(d.pop("agent_id", UNSET))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

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

        def _parse_completed_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                completed_at_type_0 = isoparse(data)

                return completed_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        completed_at = _parse_completed_at(d.pop("completed_at", UNSET))

        todo = cls(
            id=id,
            worker_id=worker_id,
            title=title,
            status=status,
            priority=priority,
            created_at=created_at,
            updated_at=updated_at,
            uuid=uuid,
            project_id=project_id,
            agent_id=agent_id,
            description=description,
            due_date=due_date,
            completed_at=completed_at,
        )

        todo.additional_properties = d
        return todo

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
