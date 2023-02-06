cd ..
python3 webserv.py config.cfg &
PID=$!
cd -
sleep 2
curl -i localhost:8070/cgibin/teststatus.py | diff - StatusAnyNumber.out 
kill $PID