cd ..
python3 webserv.py bashconfig.cfg &
PID=$!
cd -
sleep 2
curl -i localhost:8070/cgibin/testbash.sh | diff - CGIbashScript.out
kill $PID