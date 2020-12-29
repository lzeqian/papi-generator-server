currentShellDir=$(cd `dirname $0`; pwd)
kill -9 `cat ${currentShellDir}/pgs.pid`
rm -rf ${currentShellDir}/pgs.pid