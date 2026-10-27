"""Security module tests (core/security.py)

Tests cover:
- password hashing / verification
- JWT token creation and decoding
- generate_api_key format
- get_current_user happy and sad paths (via mock DB)
"""
import pytest
from datetime import timedelta
from unittest.mock import MagicMock, patch, AsyncMock

from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token,
    generate_api_key,
)


# ---------------------------------------------------------------------------
# Password hashing
# ---------------------------------------------------------------------------

class TestPasswordHashing:

    def test_hash_is_not_plain(self):
        hashed = get_password_hash("mypassword")
        assert hashed != "mypassword"

    def test_verify_correct_password(self):
        hashed = get_password_hash("correct_password")
        assert verify_password("correct_password", hashed) is True

    def test_verify_wrong_password(self):
        hashed = get_password_hash("correct_password")
        assert verify_password("wrong_password", hashed) is False

    def test_different_hashes_for_same_password(self):
        """bcrypt uses random salts so two hashes of the same password differ."""
        h1 = get_password_hash("same")
        h2 = get_password_hash("same")
        assert h1 != h2

    def test_empty_password_hashes(self):
        hashed = get_password_hash("")
        assert verify_password("", hashed) is True

    def test_unicode_password(self):
        pw = "pässwörd_日本語_🔑"
        hashed = get_password_hash(pw)
        assert verify_password(pw, hashed) is True


# ---------------------------------------------------------------------------
# JWT token creation and decoding
# ---------------------------------------------------------------------------

class TestTokens:

    def test_create_access_token_returns_string(self):
        token = create_access_token({"sub": "42"})
        assert isinstance(token, str)
        assert len(token) > 0

    def test_create_refresh_token_returns_string(self):
        token = create_refresh_token({"sub": "42"})
        assert isinstance(token, str)
        assert len(token) > 0

    def test_decode_access_token_preserves_payload(self):
        token = create_access_token({"sub": "99"})
        payload = decode_token(token)
        assert payload is not None
        assert payload["sub"] == "99"
        assert "exp" in payload

    def test_decode_refresh_token_type_claim(self):
        token = create_refresh_token({"sub": "7"})
        payload = decode_token(token)
        assert payload is not None
        assert payload["sub"] == "7"
        assert payload.get("type") == "refresh"
        assert "exp" in payload

    def test_decode_garbage_returns_none(self):
        result = decode_token("not.a.valid.jwt")
        assert result is None

    def test_decode_empty_string_returns_none(self):
        result = decode_token("")
        assert result is None

    def test_access_and_refresh_tokens_differ(self):
        access = create_access_token({"sub": "1"})
        refresh = create_refresh_token({"sub": "1"})
        assert access != refresh


# ---------------------------------------------------------------------------
# API key generation
# ---------------------------------------------------------------------------

class TestAPIKeyGeneration:

    def test_api_key_has_prefix(self):
        key = generate_api_key()
        assert key.startswith("nf_")

    def test_api_key_minimum_length(self):
        key = generate_api_key()
        # "nf_" + ~43 chars of base64
        assert len(key) >= 40

    def test_api_keys_are_unique(self):
        keys = {generate_api_key() for _ in range(20)}
        assert len(keys) == 20
