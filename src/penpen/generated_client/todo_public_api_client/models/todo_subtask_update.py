from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.todo_subtask_update_status import TodoSubtaskUpdateStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="TodoSubtaskUpdate")


@_attrs_define
class TodoSubtaskUpdate:
    """サブタスク更新リクエスト

    Attributes:
        title (str | Unset): サブタスクタイトル Example: サンプルサブタスク.
        description (None | str | Unset): サブタスクの説明 Example: これはサンプルサブタスクです.
        status (TodoSubtaskUpdateStatus | Unset): ステータス Example: completed.
        sort_order (int | Unset): 表示順序 Example: 1.
    """

    title: str | Unset = UNSET
    description: None | str | Unset = UNSET
    status: TodoSubtaskUpdateStatus | Unset = UNSET
    sort_order: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
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
        field_dict.update({})
        if title is not UNSET:
            field_dict["title"] = title
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
        title = d.pop("title", UNSET)

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        _status = d.pop("status", UNSET)
        status: TodoSubtaskUpdateStatus | Unset
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = TodoSubtaskUpdateStatus(_status)

        sort_order = d.pop("sort_order", UNSET)

        todo_subtask_update = cls(
            title=title,
            description=description,
            status=status,
            sort_order=sort_order,
        )

        todo_subtask_update.additional_properties = d
        return todo_subtask_update

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
