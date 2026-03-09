from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.todo_subtask import TodoSubtask
from ...models.todo_subtask_update import TodoSubtaskUpdate
from typing import cast



def _get_kwargs(
    subtask_id: int,
    *,
    body: TodoSubtaskUpdate,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/todo-subtasks/{subtask_id}".format(subtask_id=quote(str(subtask_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | TodoSubtask | None:
    if response.status_code == 200:
        response_200 = TodoSubtask.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | TodoSubtask]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    subtask_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: TodoSubtaskUpdate,

) -> Response[Error | TodoSubtask]:
    """ サブタスク更新

     指定IDのサブタスクを更新する

    Args:
        subtask_id (int):  Example: 1.
        body (TodoSubtaskUpdate): サブタスク更新リクエスト

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | TodoSubtask]
     """


    kwargs = _get_kwargs(
        subtask_id=subtask_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    subtask_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: TodoSubtaskUpdate,

) -> Error | TodoSubtask | None:
    """ サブタスク更新

     指定IDのサブタスクを更新する

    Args:
        subtask_id (int):  Example: 1.
        body (TodoSubtaskUpdate): サブタスク更新リクエスト

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | TodoSubtask
     """


    return sync_detailed(
        subtask_id=subtask_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    subtask_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: TodoSubtaskUpdate,

) -> Response[Error | TodoSubtask]:
    """ サブタスク更新

     指定IDのサブタスクを更新する

    Args:
        subtask_id (int):  Example: 1.
        body (TodoSubtaskUpdate): サブタスク更新リクエスト

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | TodoSubtask]
     """


    kwargs = _get_kwargs(
        subtask_id=subtask_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    subtask_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: TodoSubtaskUpdate,

) -> Error | TodoSubtask | None:
    """ サブタスク更新

     指定IDのサブタスクを更新する

    Args:
        subtask_id (int):  Example: 1.
        body (TodoSubtaskUpdate): サブタスク更新リクエスト

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | TodoSubtask
     """


    return (await asyncio_detailed(
        subtask_id=subtask_id,
client=client,
body=body,

    )).parsed
