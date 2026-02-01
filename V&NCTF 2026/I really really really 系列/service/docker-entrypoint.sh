#!/bin/bash
set -e

# 优先级设置 FLAG：A1CTF_FLAG > QUESTION_CTF_FLAG > GZCTF_FLAG > existing FLAG
if [ -n "$A1CTF_FLAG" ]; then
  export FLAG="$A1CTF_FLAG"
else
  export FLAG="VNCTF{!!!!_FLAG_ERROR_ASK_ADMIN_!!!!}"
fi

# 将FLAG写入文件 请根据需要修改
echo $FLAG | tee /flag

# 控制flag和项目源码的权限
chmod 744 /flag
# 启动 Python 应用（exec 让进程替换 shell）
if [ -x "/opt/venv/bin/python" ]; then
  exec /opt/venv/bin/python /app/app.py
else
  exec python3 /app/app.py
fi

