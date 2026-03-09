from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.todo_subtask import TodoSubtask
from ...models.todo_subtask_create import TodoSubtaskCreate
from typing import cast



def _get_kwargs(
    *,
    body: TodoSubtaskCreate,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/todo-subtasks",
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | TodoSubtask | None:
    if response.status_code == 201:
        response_201 = TodoSubtask.from_dict(response.json())



        return response_201

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

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
    *,
    client: AuthenticatedClient | Client,
    body: TodoSubtaskCreate,

) -> Response[Error | TodoSubtask]:
    """ サブタスク作成

     新しいサブタスクを作成する

    Args:
        body (TodoSubtaskCreate): サブタスク作成リクエスト

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | TodoSubtask]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient | Client,
    body: TodoSubtaskCreate,

) -> Error | TodoSubtask | None:
    """ サブタスク作成

     新しいサブタスクを作成する

    Args:
        body (TodoSubtaskCreate): サブタスク作成リクエスト

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | TodoSubtask
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: TodoSubtaskCreate,

) -> Response[Error | TodoSubtask]:
    """ サブタスク作成

     新しいサブタスクを作成する

    Args:
        body (TodoSubtaskCreate): サブタスク作成リクエスト

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | TodoSubtask]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: TodoSubtaskCreate,

) -> Error | TodoSubtask | None:
    """ サブタスク作成

     新しいサブタスクを作成する

    Args:
        body (TodoSubtaskCreate): サブタスク作成リクエスト

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | TodoSubtask
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
