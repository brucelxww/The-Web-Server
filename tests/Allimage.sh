cd ..
python3 Readimage.py & #read image files then store as binary data
python3 webserv.py config.cfg &
PID=$!
cd -
sleep 2
curl  localhost:8070/testimage1.jpg > imageoutput
sleep 2
curl  localhost:8070/testimage2.jpeg >> imageoutput
sleep 2
curl  localhost:8070/testimage3.png >> imageoutput
diff imageoutput Allimage.out 
kill $PID