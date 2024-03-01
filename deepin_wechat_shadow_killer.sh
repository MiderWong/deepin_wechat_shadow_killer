#!/usr/bin/bash
PYTHON_PATH="$HOME/.pyenv/shims/python3"
PROJECT_FOLDER="$HOME/.shell/deepin_wechat_shadow_killer/"
# 使用nohup保证关闭terminal依然运行，并将terminal输出重定向到log文件
/usr/bin/nohup "$PYTHON_PATH" "$PROJECT_FOLDER"deepin_wechat_shadow_killer.py > "$PROJECT_FOLDER"log.txt &
