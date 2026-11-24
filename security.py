from urllib.parse import urlparse

ALLOWED_SCHEMES = {"http", "https"}
BLOCKED_HOSTS = {"localhost", "127.0.0.1", "0.0.0.0", "::1"}

def validate_media_url(url: str):
    try:
        parsed = urlparse(url)
    except Exception:
        return False, "URL biçimi geçersiz."
    if parsed.scheme not in ALLOWED_SCHEMES or not parsed.hostname:
        return False, "Yalnızca http/https bağlantıları kabul edilir."
    if parsed.username or parsed.password:
        return False, "URL içine kullanıcı adı/şifre gömülmesine izin verilmiyor."
    if parsed.hostname.lower() in BLOCKED_HOSTS:
        return False, "Yerel adreslere erişim engellendi."
    if not (parsed.path.lower().endswith((".m3u8", ".mp4", ".m4v", ".webm", ".mpd"))):
        return False, "Doğrudan .m3u8, .mp4, .m4v, .webm veya .mpd bağlantısı gerekli."
    return True, "ok"
