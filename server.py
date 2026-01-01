# -*- coding: utf-8 -*-
"""
Flask エントリポイント。Supabase Auth (Google OAuth) を用い、
JWT を HttpOnly Cookie で保持し、入口で検証して Dash を保護する。
"""

import os
import secrets
import urllib.parse
from urllib.parse import urlparse
from typing import Optional

from dotenv import load_dotenv
from flask import (
    Flask,
    g,
    jsonify,
    make_response,
    redirect,
    render_template_string,
    request,
)

from app import create_app
from services.supabase_client import get_user_client

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DOTENV_PATH = os.path.join(PROJECT_ROOT, ".env")
load_dotenv(dotenv_path=DOTENV_PATH, override=False)

SUPABASE_URL = os.getenv("PUBLIC_SUPABASE_URL") or os.getenv("SUPABASE_URL") or ""
PUBLISHABLE_KEY = (
    os.getenv("PUBLIC_SUPABASE_PUBLISHABLE_DEFAULT_KEY")
    or os.getenv("SUPABASE_KEY")
    or ""
)
APP_BASE_URL = (os.getenv("APP_BASE_URL") or "").rstrip("/")
COOKIE_SECURE = os.getenv("COOKIE_SECURE", "false").lower() == "true"
COOKIE_SAMESITE = os.getenv("COOKIE_SAMESITE", "Lax")
COOKIE_DOMAIN = os.getenv("COOKIE_DOMAIN") or None

AUTH_COOKIE = "sb-access-token"
REFRESH_COOKIE = "sb-refresh-token"
STATE_COOKIE = "sb-oauth-state"


def _cookie_kwargs(http_only: bool = True, max_age: Optional[int] = None) -> dict:
    return {
        "httponly": http_only,
        "secure": COOKIE_SECURE,
        "samesite": COOKIE_SAMESITE,
        "domain": COOKIE_DOMAIN,
        "path": "/",
        **({"max_age": max_age} if max_age is not None else {}),
    }


def _get_base_url() -> str:
    """
    APP_BASE_URL を正として base URL を返す。
    Hostヘッダ偽装や、127.0.0.1 / localhost 混在でのCookie問題を避けるため、
    request.host と APP_BASE_URL の host:port が一致しない場合は例外にする。
    """
    # 本番は APP_BASE_URL 必須（Host偽装対策）
    if APP_BASE_URL:
        parsed = urlparse(APP_BASE_URL)
        expected_host = parsed.netloc
        if not expected_host:
            raise RuntimeError("APP_BASE_URL is invalid")
        if request.host != expected_host:
            raise RuntimeError(
                f"Host mismatch: expected={expected_host} actual={request.host}"
            )
        return APP_BASE_URL

    # ローカル開発のみ: 127.0.0.1 / localhost に限定して動的に採用
    if request.host in {"127.0.0.1:8050", "localhost:8050"}:
        return f"{request.scheme}://{request.host}".rstrip("/")

    raise RuntimeError("APP_BASE_URL is not set")


def _build_authorize_url(state: str, base_url: str) -> str:
    redirect_uri = f"{base_url}/auth/callback"
    params = {
        "provider": "google",
        "redirect_to": redirect_uri,
        "state": state,
    }
    return f"{SUPABASE_URL}/auth/v1/authorize?{urllib.parse.urlencode(params)}"


def _set_session_cookies(
    resp, access_token: str, refresh_token: Optional[str], expires_in: Optional[int]
) -> None:
    resp.set_cookie(
        AUTH_COOKIE, access_token, **_cookie_kwargs(http_only=True, max_age=expires_in)
    )
    if refresh_token:
        resp.set_cookie(REFRESH_COOKIE, refresh_token, **_cookie_kwargs(http_only=True))


def _clear_session_cookies(resp) -> None:
    resp.set_cookie(AUTH_COOKIE, "", **_cookie_kwargs(http_only=True, max_age=0))
    resp.set_cookie(REFRESH_COOKIE, "", **_cookie_kwargs(http_only=True, max_age=0))


def _verify_token(access_token: str):
    """Supabase Auth で検証し、ユーザー情報を返す。失敗時は None."""
    try:
        client = get_user_client(access_token)
        if not client:
            return None
        result = client.auth.get_user(access_token)
        user = getattr(result, "user", None)
        return user
    except Exception:
        return None


def _is_public_path(path: str) -> bool:
    return path.startswith(
        (
            "/auth/login",
            "/auth/callback",
            "/auth/session",
            "/auth/logout",
            "/oauth/consent",
            "/assets/",
            "/static/",
            "/_dash-component-suites/",
            "/_dash-layout",
            "/_dash-dependencies",
            "/_favicon.ico",
        )
    ) or path in {"/login", "/auth/login", "/auth/callback"}


# Flask app
flask_app = Flask(__name__)


@flask_app.before_request
def _require_auth():
    if _is_public_path(request.path):
        return None

    access_token = request.cookies.get(AUTH_COOKIE)
    if not access_token:
        return redirect("/login")

    user = _verify_token(access_token)
    if not user:
        resp = make_response(redirect("/login"))
        _clear_session_cookies(resp)
        return resp

    # 認証済み: g にセット（services 側で利用）
    g.user_id = getattr(user, "id", None)
    g.access_token = access_token
    return None


@flask_app.get("/login")
def login_page():
    return redirect("/auth/login")


@flask_app.get("/auth/login")
def auth_login():
    if not SUPABASE_URL:
        return (
            "PUBLIC_SUPABASE_URL が未設定です。.env の設定を確認してください。",
            500,
        )
    try:
        base_url = _get_base_url()
    except Exception as exc:
        return (
            f"ローカルURL不一致です。ブラウザは APP_BASE_URL に統一してください。（{exc}）",
            400,
        )
    state = secrets.token_urlsafe(16)
    url = _build_authorize_url(state, base_url)
    resp = make_response(redirect(url))
    # state は JS で参照するため HttpOnly にはしない
    resp.set_cookie(STATE_COOKIE, state, **_cookie_kwargs(http_only=False))
    return resp


@flask_app.get("/auth/callback")
def auth_callback():
    # トークンは hash フラグメントで返るため、サーバでは読めない。
    # JS で取得し /auth/session に POST する。
    try:
        _ = _get_base_url()
    except Exception as exc:
        return (
            f"ローカルURL不一致です。ブラウザは APP_BASE_URL に統一してください。（{exc}）",
            400,
        )
    html = (
        """
    <!doctype html>
    <html>
    <head><meta charset="utf-8"><title>Signing in...</title></head>
    <body>Signing in...</body>
    <script>
      const params = new URLSearchParams(window.location.hash.slice(1));
      const accessToken = params.get('access_token');
      const refreshToken = params.get('refresh_token');
      const expiresIn = Number(params.get('expires_in') || '3600');
      const state = params.get('state');
      const cookies = Object.fromEntries(document.cookie.split('; ').map(c => c.split('=')));
      const expectedState = cookies['"""
        + STATE_COOKIE
        + """'];
      if (!accessToken) {
        document.body.innerText = 'No access token returned.';
      } else if (state && expectedState && state !== expectedState) {
        document.body.innerText = 'State mismatch. Please retry login.';
      } else {
        fetch('/auth/session', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          credentials: 'include',
          body: JSON.stringify({
            access_token: accessToken,
            refresh_token: refreshToken,
            expires_in: expiresIn
          })
        }).then(async (res) => {
          if (!res.ok) {
            const t = await res.text();
            document.body.innerText = 'Failed to set session: ' + t;
            return;
          }
          document.cookie = '"""
        + STATE_COOKIE
        + """=; Max-Age=0; path=/';
          window.location.replace('/');
        }).catch(() => {
          document.body.innerText = 'Failed to set session.';
        });
      }
    </script>
    </html>
    """
    )
    return html


@flask_app.post("/auth/session")
def auth_session():
    try:
        _ = _get_base_url()
    except Exception as exc:
        return (
            f"ローカルURL不一致です。ブラウザは APP_BASE_URL に統一してください。（{exc}）",
            400,
        )
    data = request.get_json(silent=True) or {}
    access_token = data.get("access_token")
    refresh_token = data.get("refresh_token")
    expires_in = data.get("expires_in")

    if not access_token:
        return jsonify({"error": "missing access_token"}), 400

    user = _verify_token(access_token)
    if not user:
        return jsonify({"error": "invalid token"}), 401

    resp = make_response(jsonify({"ok": True}))
    _set_session_cookies(resp, access_token, refresh_token, expires_in)
    # state cookie を削除
    resp.set_cookie(STATE_COOKIE, "", **_cookie_kwargs(http_only=False, max_age=0))
    return resp


@flask_app.post("/auth/logout")
def auth_logout():
    resp = make_response(jsonify({"ok": True}))
    _clear_session_cookies(resp)
    return resp


# ---- OAuth 2.1 Authorization Path (consent UI) ----


@flask_app.get("/oauth/consent")
def oauth_consent():
    if not SUPABASE_URL:
        return (
            "PUBLIC_SUPABASE_URL が未設定です。.env の設定を確認してください。",
            500,
        )
    try:
        _ = _get_base_url()
    except Exception as exc:
        return (
            f"ローカルURL不一致です。ブラウザは APP_BASE_URL に統一してください。（{exc}）",
            400,
        )
    # Supabaseから渡されるクエリをそのまま承認リクエストに引き継ぐ
    # 型チェッカー対策: to_dict(flat=False) を使い、値は先頭要素を採用する
    raw_params = request.args.to_dict(flat=False)
    params = {
        k: (v[0] if isinstance(v, list) and v else "") for k, v in raw_params.items()
    }
    client_id = params.get("client_id", "")
    redirect_uri = params.get("redirect_uri", "")
    scope = params.get("scope", "")
    state = params.get("state", "")
    code_challenge = params.get("code_challenge", "")
    response_type = params.get("response_type", "code")

    # 承認/拒否ボタンで Supabase authorize に送り返す
    approve_params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": response_type,
        "state": state,
        "scope": scope,
        "code_challenge": code_challenge,
        "code_challenge_method": params.get("code_challenge_method", "S256"),
    }
    approve_url = (
        f"{SUPABASE_URL}/auth/v1/authorize?{urllib.parse.urlencode(approve_params)}"
    )

    deny_params = {"error": "access_denied", "state": state}
    deny_url = (
        f"{redirect_uri}?{urllib.parse.urlencode(deny_params)}" if redirect_uri else "/"
    )

    html = """
    <!doctype html>
    <html>
      <head><meta charset="utf-8"><title>Consent</title></head>
      <body style="font-family: sans-serif; max-width: 520px; margin: 40px auto;">
        <h2>アプリへのアクセスを許可しますか？</h2>
        <p>Client ID: {{client_id}}</p>
        <p>Scope: {{scope}}</p>
        <div style="margin-top:20px; display:flex; gap:10px;">
          <a href="{{approve_url}}" style="padding:10px 16px; background:#0070f3; color:#fff; text-decoration:none; border-radius:4px;">許可</a>
          <a href="{{deny_url}}" style="padding:10px 16px; background:#ccc; color:#000; text-decoration:none; border-radius:4px;">拒否</a>
        </div>
      </body>
    </html>
    """
    return render_template_string(
        html,
        client_id=client_id,
        scope=scope,
        approve_url=approve_url,
        deny_url=deny_url,
    )


# Dash を Flask にマウント
dash_app = create_app(server=flask_app)
app = dash_app.server  # for compatibility (gunicorn etc.)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    dash_app.run(host="0.0.0.0", port=port)
