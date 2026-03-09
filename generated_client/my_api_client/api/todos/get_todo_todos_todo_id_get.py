from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.http_validation_error import HTTPValidationError
from ...models.todo import Todo
from ...types import Response


def _get_kwargs(
    todo_id: int,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/todos/{todo_id}".format(
            todo_id=quote(str(todo_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Error | HTTPValidationError | Todo | None:
    if response.status_code == 200:
        response_200 = Todo.from_dict(response.json())

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


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Error | HTTPValidationError | Todo]:
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
) -> Response[Error | HTTPValidationError | Todo]:
    """TODO取得

     指定IDのTODOを取得する

    Args:
        todo_id (int): TODO ID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | HTTPValidationError | Todo]
    """

    kwargs = _get_kwargs(
        todo_id=todo_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    todo_id: int,
    *,
    client: AuthenticatedClient | Client,
) -> Error | HTTPValidationError | Todo | None:
    """TODO取得

     指定IDのTODOを取得する

    Args:
        todo_id (int): TODO ID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | HTTPValidationError | Todo
    """

    return sync_detailed(
        todo_id=todo_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    todo_id: int,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Error | HTTPValidationError | Todo]:
    """TODO取得

     指定IDのTODOを取得する

    Args:
        todo_id (int): TODO ID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | HTTPValidationError | Todo]
    """

    kwargs = _get_kwargs(
        todo_id=todo_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    todo_id: int,
    *,
    client: AuthenticatedClient | Client,
) -> Error | HTTPValidationError | Todo | None:
    """TODO取得

     指定IDのTODOを取得する

    Args:
        todo_id (int): TODO ID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | HTTPValidationError | Todo
    """

    return (
        await asyncio_detailed(
            todo_id=todo_id,
            client=client,
        )
    ).parsed
