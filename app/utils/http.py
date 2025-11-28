# app/utils/http.py
import httpx, backoff

def _giveup(e: Exception) -> bool:
    return isinstance(e, httpx.HTTPStatusError) and 400 <= e.response.status_code < 500

@backoff.on_exception(backoff.expo, (httpx.TransportError, httpx.ReadTimeout),
                      max_tries=4, jitter=backoff.full_jitter, giveup=_giveup)
def http_get(url: str, timeout_s: float = 10.0) -> httpx.Response:
    with httpx.Client(timeout=timeout_s) as c:
        r = c.get(url)
        r.raise_for_status()
        return r
