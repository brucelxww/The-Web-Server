cd ..
python3 webserv.py badconfig.cfg > ./tests/badconfigoutput
cd -
diff badconfigoutput BadConfig.out