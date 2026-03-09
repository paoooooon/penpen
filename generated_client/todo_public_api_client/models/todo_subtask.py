from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.todo_subtask_status import TodoSubtaskStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="TodoSubtask")


@_attrs_define
class TodoSubtask:
    """サブタスク情報

    Attributes:
        id (int): サブタスクID Example: 1.
        todo_id (int): 親TODOのID Example: 1.
        title (str): サブタスクタイトル Example: サンプルサブタスク.
        status (TodoSubtaskStatus): ステータス Example: todo.
        sort_order (int): 表示順序
        created_at (datetime.datetime): 作成日時 Example: 2024-01-01T00:00:00Z.
        updated_at (datetime.datetime): 更新日時 Example: 2024-01-01T00:00:00Z.
        uuid (None | Unset | UUID): UUID Example: 550e8400-e29b-41d4-a716-446655440000.
        description (None | str | Unset): サブタスクの説明 Example: これはサンプルサブタスクです.
        completed_at (datetime.datetime | None | Unset): 完了日時
    """

    id: int
    todo_id: int
    title: str
    status: TodoSubtaskStatus
    sort_order: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    uuid: None | Unset | UUID = UNSET
    description: None | str | Unset = UNSET
    completed_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        todo_id = self.todo_id

        title = self.title

        status = self.status.value

        sort_order = self.sort_order

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        uuid: None | str | Unset
        if isinstance(self.uuid, Unset):
            uuid = UNSET
        elif isinstance(self.uuid, UUID):
            uuid = str(self.uuid)
        else:
            uuid = self.uuid

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

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
                "todo_id": todo_id,
                "title": title,
                "status": status,
                "sort_order": sort_order,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if description is not UNSET:
            field_dict["description"] = description
        if completed_at is not UNSET:
            field_dict["completed_at"] = completed_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        todo_id = d.pop("todo_id")

        title = d.pop("title")

        status = TodoSubtaskStatus(d.pop("status"))

        sort_order = d.pop("sort_order")

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

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

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

        todo_subtask = cls(
            id=id,
            todo_id=todo_id,
            title=title,
            status=status,
            sort_order=sort_order,
            created_at=created_at,
            updated_at=updated_at,
            uuid=uuid,
            description=description,
            completed_at=completed_at,
        )

        todo_subtask.additional_properties = d
        return todo_subtask

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
