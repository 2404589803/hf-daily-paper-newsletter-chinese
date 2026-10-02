"""Upload unchanged JSON bytes as a file under a Feishu Wiki node."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Any

import requests


DEFAULT_BASE_URL = "https://open.feishu.cn"
MAX_SINGLE_UPLOAD_BYTES = 20 * 1024 * 1024


class FeishuApiError(RuntimeError):
    """Raised when a Feishu API request fails."""


def _response_payload(response: requests.Response) -> dict[str, Any]:
    try:
        payload = response.json()
    except ValueError as exc:
        raise FeishuApiError(
            f"Feishu returned non-JSON response (HTTP {response.status_code})"
        ) from exc

    if response.status_code >= 400:
        raise FeishuApiError(
            f"Feishu HTTP {response.status_code}: "
            f"{payload.get('msg', 'request failed')}"
        )
    if payload.get("code", 0) != 0:
        raise FeishuApiError(
            f"Feishu API error {payload.get('code')}: "
            f"{payload.get('msg', 'request failed')}"
        )
    return payload


def get_tenant_access_token(
    app_id: str, app_secret: str, base_url: str, timeout: int
) -> str:
    response = requests.post(
        f"{base_url}/open-apis/auth/v3/tenant_access_token/internal",
        json={"app_id": app_id, "app_secret": app_secret},
        timeout=timeout,
    )
    payload = _response_payload(response)
    token = payload.get("tenant_access_token")
    if not token:
        raise FeishuApiError("Feishu did not return tenant_access_token")
    return str(token)


def upload_file(
    file_path: Path,
    wiki_node_token: str,
    access_token: str,
    base_url: str,
    timeout: int,
) -> str:
    file_size = file_path.stat().st_size
    if file_size > MAX_SINGLE_UPLOAD_BYTES:
        raise FeishuApiError(
            f"{file_path} is {file_size} bytes; Feishu single-file upload "
            f"is limited to {MAX_SINGLE_UPLOAD_BYTES} bytes"
        )

    headers = {"Authorization": f"Bearer {access_token}"}
    form_data = {
        "file_name": file_path.name,
        "parent_type": "wiki",
        "parent_node": wiki_node_token,
        "size": str(file_size),
    }

    with file_path.open("rb") as source_file:
        response = requests.post(
            f"{base_url}/open-apis/drive/v1/files/upload_all",
            headers=headers,
            data=form_data,
            files={"file": (file_path.name, source_file, "application/json")},
            timeout=timeout,
        )

    payload = _response_payload(response)
    file_token = payload.get("data", {}).get("file_token")
    if not file_token:
        raise FeishuApiError("Feishu upload response did not contain file_token")
    return str(file_token)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Upload an unchanged JSON source file under a Feishu Wiki node"
    )
    parser.add_argument("--file", required=True, type=Path, help="JSON file to upload")
    parser.add_argument(
        "--timeout", type=int, default=120, help="HTTP timeout in seconds (default: 120)"
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    file_path = args.file
    if not file_path.is_file():
        raise FeishuApiError(f"File does not exist: {file_path}")

    app_id = os.environ.get("FEISHU_APP_ID", "").strip()
    app_secret = os.environ.get("FEISHU_APP_SECRET", "").strip()
    wiki_node_token = os.environ.get("FEISHU_WIKI_NODE_TOKEN", "").strip()
    base_url = os.environ.get("FEISHU_BASE_URL", DEFAULT_BASE_URL).rstrip("/")
    if not app_id or not app_secret or not wiki_node_token:
        raise FeishuApiError(
            "FEISHU_APP_ID, FEISHU_APP_SECRET, and FEISHU_WIKI_NODE_TOKEN are required"
        )

    access_token = get_tenant_access_token(
        app_id=app_id,
        app_secret=app_secret,
        base_url=base_url,
        timeout=args.timeout,
    )
    file_token = upload_file(
        file_path=file_path,
        wiki_node_token=wiki_node_token,
        access_token=access_token,
        base_url=base_url,
        timeout=args.timeout,
    )
    print(f"Uploaded {file_path} to Feishu; file_token={file_token}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FeishuApiError, OSError, requests.RequestException) as exc:
        print(f"Feishu upload failed: {exc}")
        raise SystemExit(1)
