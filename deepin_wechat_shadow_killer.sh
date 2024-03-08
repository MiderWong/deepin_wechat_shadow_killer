#!/usr/bin/bash
# !!!注意：为确保脚本正常使用，这里的路径请使用绝对路径
PYTHON_PATH="/usr/bin/python3"
PROJECT_FOLDER=""
# 使用nohup保证关闭terminal依然运行，并将terminal输出重定向到log文件
cd "$PROJECT_FOLDER" && /usr/bin/nohup "$PYTHON_PATH" "$PROJECT_FOLDER"deepin_wechat_shadow_killer.py > "$PROJECT_FOLDER"log.txt &
