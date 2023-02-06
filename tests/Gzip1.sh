cd ..
python3 webserv.py config.cfg &
PID=$!
cd -
sleep 2
curl -H 'Accept-encoding: gzip' --output - localhost:8070/cgibin/hello.py > Gzipoutput1
zcat Gzipoutput1 | diff - gzip.out 
kill $PID