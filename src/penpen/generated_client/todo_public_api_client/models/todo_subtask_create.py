from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.todo_subtask_create_status import TodoSubtaskCreateStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="TodoSubtaskCreate")


@_attrs_define
class TodoSubtaskCreate:
    """サブタスク作成リクエスト

    Attributes:
        todo_id (int): 親TODOのID Example: 1.
        title (str): サブタスクタイトル Example: サンプルサブタスク.
        description (None | str | Unset): サブタスクの説明 Example: これはサンプルサブタスクです.
        status (TodoSubtaskCreateStatus | Unset): ステータス Default: TodoSubtaskCreateStatus.TODO. Example: todo.
        sort_order (int | Unset): 表示順序 Default: 0.
    """

    todo_id: int
    title: str
    description: None | str | Unset = UNSET
    status: TodoSubtaskCreateStatus | Unset = TodoSubtaskCreateStatus.TODO
    sort_order: int | Unset = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        todo_id = self.todo_id

        title = self.title

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        status: str | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        sort_order = self.sort_order

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "todo_id": todo_id,
                "title": title,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if status is not UNSET:
            field_dict["status"] = status
        if sort_order is not UNSET:
            field_dict["sort_order"] = sort_order

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        todo_id = d.pop("todo_id")

        title = d.pop("title")

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        _status = d.pop("status", UNSET)
        status: TodoSubtaskCreateStatus | Unset
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = TodoSubtaskCreateStatus(_status)

        sort_order = d.pop("sort_order", UNSET)

        todo_subtask_create = cls(
            todo_id=todo_id,
            title=title,
            description=description,
            status=status,
            sort_order=sort_order,
        )

        todo_subtask_create.additional_properties = d
        return todo_subtask_create

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
