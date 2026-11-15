#!/usr/bin/env python3
"""
The Unofficial Guide — the same pipeline, over HTTP.

    python serve.py                          run it locally on port 5000
    gunicorn serve:app                       run it the way a host runs it

Nothing new happens in this file. It is a wrapper: a request comes in, it
hands the question to `app.py::ask_pipeline` — the exact function the command
line uses — and hands the answer back as JSON. Retrieval, the relevance gate
and the grounded prompt all still live where they lived. If you change how
your system answers, you change it in those files and this one follows.

Two routes:

    POST /ask       {"question": "..."} in, the answer and its sources out
    GET  /health    is the service up, and is there an index to search

Why this exists: `app.py` runs once and exits, which is fine on your laptop
and impossible to deploy. A hosted service has to stay up and wait for
requests. This is the smallest thing that does that.

Each request is recorded as one JSON object in `results/service_runs.jsonl`.
The record includes the input, output, status, latency, sources, and the token
usage measured during that request.
"""

import datetime as dt
import json
import os
import time

from flask import Flask, jsonify, request

import config

app = Flask(__name__)


def _write_service_log(record: dict) -> None:
    config.SERVICE_LOG.parent.mkdir(exist_ok=True)
    with config.SERVICE_LOG.open("a", encoding="utf-8") as log:
        log.write(json.dumps(record, ensure_ascii=True) + "\n")


def _usage_delta(before: dict[str, int], after: dict[str, int]) -> dict[str, int]:
    return {
        key: after.get(key, 0) - before.get(key, 0)
        for key in ("prompt", "output", "total")
    }


@app.get("/health")
def health():
    """Is the service up, and is there an index to search?

    Two different questions, and the second one is the one that bites. A
    freshly deployed service answers this route happily while every /ask
    returns "no index" — hosts give you no disk that survives a restart, so
    the index has to be built as part of getting the service up. Checking
    here means you find that out in one request instead of five.
    """
    from store import index_exists

    ready = index_exists(config.CORPUS)
    return jsonify(
        {
            "status": "ok",
            "corpus": config.CORPUS,
            "index_ready": ready,
            "detail": (
                "ready"
                if ready
                else "no index for this corpus — run `python app.py index`"
            ),
        }
    )


@app.post("/ask")
def ask():
    """One question in, one grounded answer out.

    A refused question is a 200, not an error. The gate refusing is your
    system working — it is an answer, and the JSON says so with
    `"refused": true` so whatever calls this can tell the two apart.
    """
    from app import ask_pipeline
    import generate

    started = time.perf_counter()
    usage_before = generate.token_counts()
    payload = request.get_json(silent=True) or {}
    question = (payload.get("question") or "").strip()

    if not question:
        _write_service_log(
            {
                "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
                "endpoint": "/ask",
                "question": "",
                "answer": None,
                "status_code": 400,
                "latency_ms": round((time.perf_counter() - started) * 1000, 2),
                "refused": False,
                "sources": [],
                "token_usage": _usage_delta(usage_before, generate.token_counts()),
            }
        )
        return (
            jsonify(
                {
                    "error": "Send JSON with a question in it, like "
                    '{"question": "is the housing lottery random?"}'
                }
            ),
            400,
        )

    try:
        outcome = ask_pipeline(question, corpus=config.CORPUS)
    except Exception as exc:  # noqa: BLE001 — a reader gets this, not a traceback
        _write_service_log(
            {
                "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
                "endpoint": "/ask",
                "question": question,
                "answer": None,
                "status_code": 500,
                "latency_ms": round((time.perf_counter() - started) * 1000, 2),
                "refused": False,
                "sources": [],
                "error": f"{type(exc).__name__}: {exc}",
                "token_usage": _usage_delta(usage_before, generate.token_counts()),
            }
        )
        return jsonify({"error": f"{type(exc).__name__}: {exc}"}), 500

    token_usage = _usage_delta(usage_before, generate.token_counts())
    _write_service_log(
        {
            "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
            "endpoint": "/ask",
            "question": question,
            "answer": outcome["answer"],
            "status_code": 200,
            "latency_ms": round((time.perf_counter() - started) * 1000, 2),
            "refused": outcome["refused"],
            "sources": outcome["sources"],
            "best_distance": round(outcome["best_distance"], 4),
            "threshold": outcome["threshold"],
            "token_usage": token_usage,
        }
    )
    return jsonify(
        {
            "question": question,
            "answer": outcome["answer"],
            "refused": outcome["refused"],
            "sources": outcome["sources"],
            "best_distance": round(outcome["best_distance"], 4),
            "threshold": outcome["threshold"],
            "corpus": config.CORPUS,
            "token_usage": token_usage,
        }
    )


def main():
    # Hosts tell you which port to listen on through PORT, and they expect you
    # on 0.0.0.0. Binding 127.0.0.1 instead works perfectly on your laptop and
    # then answers nothing at all once deployed, because the host's router
    # can't reach a socket that only accepts connections from inside the
    # container. It is the single most common way a first deploy "succeeds"
    # and is unreachable.
    port = int(os.getenv("PORT", "5000"))

    # Debug mode reloads on save, which is handy, and prints a console that
    # runs arbitrary code, which is not something to leave switched on where
    # strangers can reach it. Off unless you ask for it.
    debug = os.getenv("AI201_DEBUG", "0") == "1"

    print(f"Serving The Unofficial Guide on http://localhost:{port}")
    print(f"Corpus: {config.CORPUS}    (Ctrl-C to stop)\n")
    print("Try it from another terminal:\n")
    print(f"  curl http://localhost:{port}/health")
    print(
        f"  curl -X POST http://localhost:{port}/ask \\\n"
        f"    -H 'Content-Type: application/json' \\\n"
        f"    -d '{{\"question\": \"is the housing lottery random?\"}}'\n"
    )

    app.run(host="0.0.0.0", port=port, debug=debug)


if __name__ == "__main__":
    main()
