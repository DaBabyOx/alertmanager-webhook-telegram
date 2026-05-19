#!/bin/sh
set -e

if [ -z "${BASIC_AUTH_USERNAME:-}" ]; then
  echo "warning: BASIC_AUTH_USERNAME is not set"
else
  echo "BASIC_AUTH_USERNAME is set"
fi

if [ -z "${BASIC_AUTH_PASSWORD:-}" ]; then
  echo "warning: BASIC_AUTH_PASSWORD is not set"
else
  echo "BASIC_AUTH_PASSWORD is set"
fi

if [ -z "${TELEGRAM_BOTTOKEN:-}" ]; then
  echo "FAIL: TELEGRAM_BOTTOKEN is not set"
  exit 1
else
  echo "TELEGRAM_BOTTOKEN is set"
fi

if [ -z "${TELEGRAM_CHATID:-}" ]; then
  echo "FAIL: TELEGRAM_CHATID is not set"
  exit 2
else
  echo "TELEGRAM_CHATID is set"
fi

exec gunicorn -w 4 -b 0.0.0.0:9119 flaskAlert:app
