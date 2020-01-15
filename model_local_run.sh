num=$1
workdir=$2
outdir=$3
for ((i=0 ; i <= $num ; i++)); do
   sh model_local.sh $i $workdir $outdir &
done
echo Finished
