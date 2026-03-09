from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.todo import Todo
from ...models.todo_update import TodoUpdate
from typing import cast



def _get_kwargs(
    todo_id: int,
    *,
    body: TodoUpdate,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/todos/{todo_id}".format(todo_id=quote(str(todo_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | Todo | None:
    if response.status_code == 200:
        response_200 = Todo.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | Todo]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    todo_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: TodoUpdate,

) -> Response[Error | Todo]:
    """ TODO更新

     指定IDのTODOを更新する

    Args:
        todo_id (int):  Example: 1.
        body (TodoUpdate): TODO更新リクエスト

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Todo]
     """


    kwargs = _get_kwargs(
        todo_id=todo_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    todo_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: TodoUpdate,

) -> Error | Todo | None:
    """ TODO更新

     指定IDのTODOを更新する

    Args:
        todo_id (int):  Example: 1.
        body (TodoUpdate): TODO更新リクエスト

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Todo
     """


    return sync_detailed(
        todo_id=todo_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    todo_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: TodoUpdate,

) -> Response[Error | Todo]:
    """ TODO更新

     指定IDのTODOを更新する

    Args:
        todo_id (int):  Example: 1.
        body (TodoUpdate): TODO更新リクエスト

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Todo]
     """


    kwargs = _get_kwargs(
        todo_id=todo_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    todo_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: TodoUpdate,

) -> Error | Todo | None:
    """ TODO更新

     指定IDのTODOを更新する

    Args:
        todo_id (int):  Example: 1.
        body (TodoUpdate): TODO更新リクエスト

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Todo
     """


    return (await asyncio_detailed(
        todo_id=todo_id,
client=client,
body=body,

    )).parsed
