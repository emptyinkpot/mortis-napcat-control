#!/usr/bin/env python3
import argparse
import base64
import os
import subprocess
import sys


REPO_PATH = "/home/ubuntu/multica-public-watch/repo"
REPO_URL = "https://github.com/emptyinkpot/mortis-multica-watch"
NOTIFY_PATH = "/home/ubuntu/multica-public-watch/control/notify.py"


def decode_b64(value: str) -> str:
    return base64.b64decode(value.encode("utf-8")).decode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Send a whitelisted NapCat group message through host notify.py")
    parser.add_argument("--group-id", required=True)
    parser.add_argument("--message-b64", required=True)
    parser.add_argument("--source-b64", default="")
    args = parser.parse_args()

    message = decode_b64(args.message_b64).strip()
    source = decode_b64(args.source_b64).strip() if args.source_b64 else "mortis-ai"
    if not message:
        raise SystemExit("message is empty")

    env = dict(os.environ)
    env.update(
        {
            "NOTIFY_ENABLED": "1",
            "NOTIFY_DRY_RUN": "0",
            "NOTIFY_CHANNELS": "napcat",
            "NAPCAT_MESSAGE_MODE": "group",
            "NAPCAT_GROUP_ID": args.group_id.strip(),
            "NAPCAT_TRANSPORT": "webui",
            "NAPCAT_WEBUI_URL": "http://127.0.0.1:16099",
            "NAPCAT_WEBUI_CONFIG_PATH": "/home/ubuntu/napcat/data/config/webui.json",
        }
    )

    command = [
        "python3",
        NOTIFY_PATH,
        "--repo-path",
        REPO_PATH,
        "--repo-url",
        REPO_URL,
        "--source",
        source,
        "--test-message",
        message,
    ]

    result = subprocess.run(command, env=env, text=True, capture_output=True)
    if result.stdout:
        sys.stdout.write(result.stdout)
    if result.stderr:
        sys.stderr.write(result.stderr)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
