currentShellDir=$(cd `dirname $0`; pwd)
if [ -f ${currentShellDir}/pgs.pid ];then
  echo "程序已启动，无法再次启动"
  exit 1
fi
cd ${currentShellDir}/../
if [ ! -d ${currentShellDir}/../logs ];then
  mkdir -p ${currentShellDir}/../logs
fi
nohup python3 historymain.py >${currentShellDir}/../logs/catalina.out 2>&1 & echo $! >> ${currentShellDir}/pgs.pid
