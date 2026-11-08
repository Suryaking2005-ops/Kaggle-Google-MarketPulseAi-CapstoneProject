import pytest

from marketpulse import config


def test_missing_key_raises(monkeypatch):
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    with pytest.raises(config.MissingAPIKeyError):
        config.get_api_key()


def test_placeholder_key_is_rejected(monkeypatch):
    monkeypatch.setenv("GOOGLE_API_KEY", "your_gemini_api_key_here")
    with pytest.raises(config.MissingAPIKeyError):
        config.get_api_key()


def test_real_looking_key_is_returned(monkeypatch):
    monkeypatch.setenv("GOOGLE_API_KEY", "abc123")
    assert config.get_api_key() == "abc123"
