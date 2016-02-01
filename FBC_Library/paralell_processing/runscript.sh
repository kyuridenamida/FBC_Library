pgrep python | xargs kill -9
core=`cat /proc/cpuinfo | grep processor | wc -l`
for x in `seq 1 $core`
do
	client.py & 
done