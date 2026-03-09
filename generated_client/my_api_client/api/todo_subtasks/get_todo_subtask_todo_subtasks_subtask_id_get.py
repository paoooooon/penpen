from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.http_validation_error import HTTPValidationError
from ...models.todo_subtask import TodoSubtask
from typing import cast



def _get_kwargs(
    subtask_id: int,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/todo-subtasks/{subtask_id}".format(subtask_id=quote(str(subtask_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | HTTPValidationError | TodoSubtask | None:
    if response.status_code == 200:
        response_200 = TodoSubtask.from_dict(response.json())



        return response_200

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())



        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | HTTPValidationError | TodoSubtask]:
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

) -> Response[Error | HTTPValidationError | TodoSubtask]:
    """ サブタスク取得

     指定IDのサブタスクを取得する

    Args:
        subtask_id (int): サブタスクID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | HTTPValidationError | TodoSubtask]
     """


    kwargs = _get_kwargs(
        subtask_id=subtask_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    subtask_id: int,
    *,
    client: AuthenticatedClient | Client,

) -> Error | HTTPValidationError | TodoSubtask | None:
    """ サブタスク取得

     指定IDのサブタスクを取得する

    Args:
        subtask_id (int): サブタスクID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | HTTPValidationError | TodoSubtask
     """


    return sync_detailed(
        subtask_id=subtask_id,
client=client,

    ).parsed

async def asyncio_detailed(
    subtask_id: int,
    *,
    client: AuthenticatedClient | Client,

) -> Response[Error | HTTPValidationError | TodoSubtask]:
    """ サブタスク取得

     指定IDのサブタスクを取得する

    Args:
        subtask_id (int): サブタスクID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | HTTPValidationError | TodoSubtask]
     """


    kwargs = _get_kwargs(
        subtask_id=subtask_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    subtask_id: int,
    *,
    client: AuthenticatedClient | Client,

) -> Error | HTTPValidationError | TodoSubtask | None:
    """ サブタスク取得

     指定IDのサブタスクを取得する

    Args:
        subtask_id (int): サブタスクID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | HTTPValidationError | TodoSubtask
     """


    return (await asyncio_detailed(
        subtask_id=subtask_id,
client=client,

    )).parsed
