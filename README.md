# Todo API クライアント

Todo管理 API の Python クライアント（非同期 + Pydantic V2 対応）。

## 特徴

- **非同期 (async/await)** 対応 (httpx 使用)
- **Pydantic V2** による型安全性
- OpenAPI 仕様から自動生成

## インストール

```bash
pip install httpx httpx[http2] pydantic
```

## クライアント生成

### コンテナ内で実行する場合

```bash
# OpenAPI 仕様をダウンロード
make download-spec API_URL=http://172.17.0.1:10000

# クライアントを生成（非同期 + Pydantic V2）
make generate-client
```

### コンテナ外から実行する場合 (docker-compose 使用)

```bash
# OpenAPI 仕様をダウンロード
docker-compose exec app make download-spec API_URL=http://host.docker.internal:10000

# クライアントを生成
docker-compose exec app make generate-client
```

## 使用例

```python
import asyncio
from todo_api_client import AsyncClient
from todo_api_client.models import ProjectCreate

async def main():
    async with AsyncClient(base_url="http://172.17.0.1:10000") as client:
        # ヘルスチェック
        health = await client.health_health_get()
        print(health)

        # プロジェクト一覧
        projects = await client.list_projects_projects_get()
        for p in projects:
            print(p)

        # プロジェクト作成
        new_project = await client.create_project_projects_post(
            body=ProjectCreate(name="マイプロジェクト", description="サンプルプロジェクト")
        )
        print(new_project)

asyncio.run(main())
```

## Makefile コマンド

| コマンド | 説明 |
|---------|------|
| `make download-spec` | API から OpenAPI 仕様をダウンロード |
| `make generate-client` | 非同期 Python クライアントを生成 |
| `make clean` | 生成ファイルを削除 |
| `make format` | 生成コードをフォーマット |