#!/bin/bash
. DeployementConfigs/confData.conf

echo Start Automated Optimization Process


poolSize=$1
logFileSize=$2
flushMethod=$3
threadCache=$4
threadSleep=$5
maxConnect=$6

fileVar=$7




completeResult=${completeResult}
summaryReport=${summaryReport}
testScript=${testScript}
overallCsv=${overallCsv}
localSummary=${localSummary}
dbConf=${dbConf}
identityServer=${identityServer}

testConcurrency=${testConcurrency}
testTime=${testTime}
warmUpTime=${warmUpTime}



sudo sed  -i '/^innodb_buffer_pool_size=/s/=.*/='${poolSize}'M/' ${dbConf}
echo "Updated buffer size to " ${poolSize}
sudo sed  -i '/^innodb_log_file_size=/s/=.*/='${logFileSize}'M/' ${dbConf}
echo "Updated log file size to " ${logFileSize}
sudo sed  -i '/^innodb_flush_method=/s/=.*/='${flushMethod}'/' ${dbConf}
echo "Updated flushMethod to " ${flushMethod}
sudo sed  -i '/^thread_cache_size=/s/=.*/='${threadCache}'/' ${dbConf}
echo "Updated threadCache to " ${threadCache}
sudo sed  -i '/^innodb_thread_sleep_delay=/s/=.*/='${threadSleep}'/' ${dbConf}
echo "Updated innodb_thread_sleep_delay to " ${threadSleep}
sudo sed  -i '/^max_connections=/s/=.*/='${maxConnect}'/' ${dbConf}
echo "Updated max_connections to " ${maxConnect}

echo "Starting MySql server"
sudo service mysql start 


mysql -u root -proot -e "quit"
sleep 20s
echo -e "Connected to MySql server as Admin"


echo -e "Starting wso2 IS server"
gnome-terminal -- /bin/sh -c 'sudo -S ${identityServer}'
sleep 80s

statusCode=$(curl -s -o /dev/null -I -k --insecure -w "%{http_code}" https://localhost:9443/carbon/)
while [[ $statusCode == 500 ]] || [[ $statusCode == 000 ]]; do
echo "$statusCode"
sleep 10s
statusCode=$(curl -s -o /dev/null -I -k --insecure -w "%{http_code}" https://localhost:9443/carbon/)
done

sudo docker run  --network=host --interactive --tty --rm --volume `pwd`/TestData:/jmeter egaillardon/jmeter-plugins -n -t ${testScript} -Jconcurrency=${testConcurrency} -Jtime=${testTime} -l  ${completeResult}$fileVar.jtl
sleep 5s
	
sudo docker run --interactive --tty --rm --volume `pwd`/TestData:/jmeter egaillardon/jmeter-plugins JMeterPluginsCMD.sh --tool Reporter --generate-csv ${summaryReport}$fileVar.csv --input-jtl ${completeResult}$fileVar.jtl --start-offset ${warmUpTime} --plugin-type AggregateReport

echo -e "Stop the wso2 IS server"
sudo sh ${identityServer} --stop
sleep 10s

echo -e "Stop the MySql server"
sudo service mysql stop
sleep 10s


average_latency="$(tail -1 ${localSummary}$fileVar.csv | awk -F, '{print $3}')"
result_99="$(tail -1 ${localSummary}$fileVar.csv | awk -F, '{print $7}')"
result_throughput="$(tail -1 ${localSummary}$fileVar.csv | awk -F, '{print $11}')"

echo "$fileVar,$poolSize,$logFileSize,$flushMethod,$threadCache,$threadSleep,$maxConnect,$average_latency,$result_99,$result_throughput" >> $overallCsv












	
	
	
	
	
	


	

	




