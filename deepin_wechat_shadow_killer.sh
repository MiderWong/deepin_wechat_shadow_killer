#!/usr/bin/bash
PYTHON_PATH="/home/Jason/.pyenv/shims/python3"
PROJECT_FOLDER="/home/Jason/.shell/deepin_wechat_shadow_killer/"
/usr/bin/nohup "$PYTHON_PATH" "$PROJECT_FOLDER"deepin_wechat_shadow_killer.py > "$PROJECT_FOLDER"log.txt &
