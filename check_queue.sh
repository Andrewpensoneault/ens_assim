nameof=$1
while true; do
stats=`qstat -u apensoneault`
if [[ $stats == *$nameof* ]]; then
  sleep 3
else
break
fi
done
