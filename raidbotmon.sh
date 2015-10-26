# A monitor script for bot that restarts bot if it crashes. Only for production use.

control_c() {
    kill -9 $PID
    exit
}

trap control_c SIGINT

until python raidbot.py; do
    PID=$!
    echo "'raidbot.py' crashed with exit code $?. Restarting..." >&2
    sleep 1
done