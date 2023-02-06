About the programming:
Main construction:read config file,create socket,parse request,deal with static file or CGI program,send data,close connection,then accept new connection again
Code is commented clearly. :)

About the Extension:
Extension: Compressed packets to send back to the browser.
How it works:Check whether the request asks a "gzip" content-type for return,if yes,then compress the data body,send the compressed data to client.

Description of testcases:
Allimage.sh: test files with the extension "jpg" "jpeg" "png"
AnyCustomStatus.sh: test status code with any number
BadConfig.sh: config file misses content
CGIbashScript.sh : test with bash CGI programs
Gzip1.sh: test gzip function with static file
Gzip2.sh: test gzip function with CGI programs
Static+CGI.sh: test the function of the server with static files and CGI programs
(Functions those have been tested through ed like 404/505 error won't be tested here.)