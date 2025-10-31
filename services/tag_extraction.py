"""Extract product tags from structured data and descriptions."""

import json
import os
import time
from typing import Any, Dict, Iterable, List, Optional

import requests
from retrying import retry

IO_API_URL = os.getenv(
    "IO_INTELLIGENCE_API_URL",
    "https://api.intelligence.io.solutions/api/v1/chat/completions",
)
IO_API_KEY = os.getenv("IO_INTELLIGENCE_API_KEY")
IO_MODEL = os.getenv("IO_INTELLIGENCE_MODEL", "meta-llama/Llama-3.2-90B-Vision-Instruct")
IO_TIMEOUT = int(os.getenv("IO_INTELLIGENCE_TIMEOUT", "10"))
DEFAULT_TAG_COUNT = 10


def _format_product_candidates(candidates: Iterable[Dict[str, Any]]) -> str:
    lines: List[str] = []
    for idx, item in enumerate(candidates, start=1):
        if not isinstance(item, dict):
            continue
        name = item.get("name") or ""
        shop = item.get("shopName") or ""
        price = item.get("price")
        jan = item.get("jan") or ""
        code = item.get("itemCode") or ""
        parts = [f"#{idx}"]
        if name:
            parts.append(f"Name: {name}")
        if shop:
            parts.append(f"Shop: {shop}")
        if price is not None:
            parts.append(f"Price: {price}")
        if jan:
            parts.append(f"JAN: {jan}")
        if code:
            parts.append(f"ItemCode: {code}")
        lines.append(" | ".join(parts))
    return "\n".join(lines)


def _parse_tags(raw_text: str) -> List[str]:
    raw_text = raw_text.strip()
    if not raw_text:
        return []

    try:
        parsed = json.loads(raw_text)
        if isinstance(parsed, list):
            return [str(tag).strip() for tag in parsed if str(tag).strip()]
        if isinstance(parsed, dict) and "tags" in parsed:
            tags = parsed["tags"]
            if isinstance(tags, list):
                return [str(tag).strip() for tag in tags if str(tag).strip()]
    except json.JSONDecodeError:
        pass

    separators = ["\n", ",", "・", "|"]
    candidates = [raw_text]
    for sep in separators:
        temp: List[str] = []
        for chunk in candidates:
            temp.extend(chunk.split(sep))
        candidates = temp
    return [tag.strip().strip("-•") for tag in candidates if tag.strip()]


def extract_tags(
    product_candidates: List[Dict[str, Any]], description: Optional[str]
) -> Dict[str, Any]:
    """Generate tags using product search results and description text."""

    print(f"DEBUG: extract_tags called with candidates: {len(product_candidates) if product_candidates else 0}, description: {bool(description)}")

    if not IO_API_KEY:
        print("DEBUG: IO_API_KEY is not set")
        return {
            "status": "missing_credentials",
            "tags": [],
            "message": "IO Intelligence APIキーが設定されていません。",
        }

    if not product_candidates and not description:
        print("DEBUG: No candidates and no description")
        return {
            "status": "not_ready",
            "tags": [],
            "message": "タグ抽出に必要な情報が不足しています。",
        }

    formatted_candidates = _format_product_candidates(product_candidates)
    description_text = description or ""

    print(f"DEBUG: formatted_candidates: {bool(formatted_candidates)}, description_text: {bool(description_text)}")

    # 楽天APIテキストと画像説明から別々にタグを生成
    all_tags = []

    # 楽天APIの結果がある場合、最大5個のタグを生成
    if product_candidates:
        print("DEBUG: Extracting tags from Rakuten API data")
        rakuten_tags = _extract_tags_from_text(formatted_candidates, "product_info", 5)
        if rakuten_tags:
            all_tags.extend(rakuten_tags)
            print(f"Generated {len(rakuten_tags)} tags from Rakuten API data: {rakuten_tags}")

    # 画像説明がある場合、最大5個のタグを生成
    if description_text:
        print(f"DEBUG: Extracting tags from image description: {description_text[:100]}...")
        image_tags = _extract_tags_from_text(description_text, "image_description", 5)
        if image_tags:
            all_tags.extend(image_tags)
            print(f"Generated {len(image_tags)} tags from image description: {image_tags}")

    print(f"DEBUG: Total tags before deduplication: {len(all_tags)}")

    # 重複を除去し、最大10個に制限
    unique_tags = []
    seen = set()
    for tag in all_tags:
        tag_lower = tag.lower()
        if tag_lower not in seen:
            seen.add(tag_lower)
            unique_tags.append(tag)

    final_tags = unique_tags[:10]

    if not final_tags:
        return {
            "status": "error",
            "tags": [],
            "message": "タグを生成できませんでした。",
        }

    return {
        "status": "success",
        "tags": final_tags,
        "message": f"{len(final_tags)}個のタグ候補を生成しました。",
    }


def _extract_tags_from_text(text: str, source_type: str, max_tags: int) -> List[str]:
    """指定されたテキストからタグを抽出"""
    if not text or not text.strip():
        return []

    if source_type == "product_info":
        instructions = (
            "以下の商品情報をもとに、推し活グッズ管理に役立つ日本語タグを生成してください。"
            "タグは製品カテゴリ、キャラクター名、作品名、素材、色、イベント名など利用者が絞り込みに使える語を中心にしてください。"
            f"タグは最大{max_tags}個、重複しないように。"
            '返答は JSON 配列 (例: ["タグ1", "タグ2"]) のみで行ってください。'
        )
        prompt = f"# 商品情報\n{text}\n\n# 指示\n{instructions}"
    else:  # image_description
        instructions = (
            "以下の画像説明をもとに、推し活グッズ管理に役立つ日本語タグを生成してください。"
            "タグは製品カテゴリ、キャラクター名、作品名、素材、色、イベント名など利用者が絞り込みに使える語を中心にしてください。"
            f"タグは最大{max_tags}個、重複しないように。"
            '返答は JSON 配列 (例: ["タグ1", "タグ2"]) のみで行ってください。'
        )
        prompt = f"# 画像説明\n{text}\n\n# 指示\n{instructions}"

    prompt_length = len(prompt)
    print(f"IO API _extract_tags_from_text ({source_type}): prompt length = {prompt_length} characters")

    payload = {
        "model": IO_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You extract concise tags for merchandise inventory systems.",
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
    }

    headers = {
        "Authorization": f"Bearer {IO_API_KEY}",
        "Content-Type": "application/json",
    }

    @retry(
        stop_max_attempt_number=3,
        wait_fixed=2000,
        retry_on_exception=lambda exc: isinstance(exc, requests.RequestException),
    )
    def _call_api():
        print(f"IO API _extract_tags_from_text ({source_type}): sending request with timeout={IO_TIMEOUT}s")
        start_time = time.time()
        response = requests.post(
            IO_API_URL, headers=headers, json=payload, timeout=IO_TIMEOUT
        )
        response.raise_for_status()
        elapsed = time.time() - start_time
        print(f"IO API _extract_tags_from_text ({source_type}): response received in {elapsed:.2f}s")
        return response

    try:
        response = _call_api()
    except requests.RequestException as exc:  # pragma: no cover - ネットワーク依存
        print(f"IO API _extract_tags_from_text ({source_type}): API call failed: {exc}")
        return []

    try:
        payload = response.json()
    except ValueError as exc:  # pragma: no cover - JSON解析エラー
        print(f"IO API _extract_tags_from_text ({source_type}): JSON parse failed: {exc}")
        return []

    try:
        content = payload["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        print(f"IO API _extract_tags_from_text ({source_type}): No content in response")
        return []

    if isinstance(content, list):
        text_parts: List[str] = []
        for entry in content:
            if isinstance(entry, dict) and entry.get("type") in {"output_text", "text"}:
                text_parts.append(str(entry.get("text", "")))
        raw_text = "\n".join(text_parts).strip()
    else:
        raw_text = str(content).strip()

    tags = _parse_tags(raw_text)
    return tags[:max_tags] if tags else []
