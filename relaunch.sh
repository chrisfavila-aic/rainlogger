if ! [ "$(ps -ax | grep "[r]ainlogger.py")" ]; then
    /usr/bin/python /home/pi/rainlogger.py &
fi
