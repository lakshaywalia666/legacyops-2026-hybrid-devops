import json
import os
import signal
import sys
import time

import redis
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
JOB_QUEUE = os.getenv("LEGACYOPS_JOB_QUEUE", "legacyops:jobs")
POLL_TIMEOUT_SECONDS = int(os.getenv("WORKER_POLL_TIMEOUT_SECONDS", "5"))

running = True


def shutdown_handler(signum, frame):
    global running
    print(f"received signal {signum}; shutting down gracefully", flush=True)
    running = False


signal.signal(signal.SIGTERM, shutdown_handler)
signal.signal(signal.SIGINT, shutdown_handler)


def process_job(job: dict) -> None:
    job_type = job.get("type")
    payload = job.get("payload", {})

    if job_type == "order_created":
        print(
            json.dumps(
                {
                    "event": "worker_processed_order_created",
                    "order_id": payload.get("order_id"),
                    "customer_id": payload.get("customer_id"),
                    "processed_at": int(time.time()),
                }
            ),
            flush=True,
        )
        return

    print(
        json.dumps(
            {
                "event": "worker_unknown_job_type",
                "job_type": job_type,
                "payload": payload,
            }
        ),
        flush=True,
    )


def main() -> int:
    print(
        json.dumps(
            {
                "event": "worker_starting",
                "redis_url": REDIS_URL,
                "queue": JOB_QUEUE,
            }
        ),
        flush=True,
    )

    client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

    while running:
        try:
            item = client.brpop(JOB_QUEUE, timeout=POLL_TIMEOUT_SECONDS)
            if item is None:
                print(json.dumps({"event": "worker_idle"}), flush=True)
                continue

            _, raw_job = item
            job = json.loads(raw_job)
            process_job(job)

        except redis.exceptions.ConnectionError as exc:
            print(json.dumps({"event": "redis_connection_error", "error": str(exc)}), flush=True)
            time.sleep(5)

        except Exception as exc:
            print(json.dumps({"event": "worker_error", "error": str(exc)}), flush=True)
            time.sleep(2)

    print(json.dumps({"event": "worker_stopped"}), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
