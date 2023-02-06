cd ..
python3 webserv.py config.cfg &
PID=$!
cd -
sleep 2
curl -H 'Accept-encoding: gzip' --output - localhost:8070/greetings.html > Gzipoutput2
zcat Gzipoutput2 | diff - Gzip2.out 
kill $PID