cd ..
python3 webserv.py config.cfg &
PID=$!
cd -
sleep 2
curl -i localhost:8070/home.js > staticcgioutput
sleep 2
curl -i localhost:8070/info1112.txt >> staticcgioutput
sleep 2
curl -i localhost:8070/cgibin/hello.py >> staticcgioutput
sleep 2
curl -i localhost:8070/ >> staticcgioutput
diff staticcgioutput Static+CGI.out
kill $PID