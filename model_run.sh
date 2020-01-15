ensnum=$1
workdir=$2
outdir=$3
jobname=$4
if [ -z "$SGE_O_HOST" ]
then
#	qsub -N $jobname -e /dev/null -o /dev/null -q  -l h_vmem=6G -pe smp 1 -cwd -t 1:$ensnum model.sh $workdir $outdir
	qsub -N $jobname -e /dev/null -o /dev/null -q all.q -l cpu_arch=skylake_silver -l h_vmem=6G -pe smp 1 -cwd -t 1:$ensnum model.sh $workdir $outdir
else
#	ssh $SGE_O_HOST "cd $SGE_O_WORKDIR/../Code && qsub -N $jobname -e /dev/null -o /dev/null -q  -l h_vmem=6G -pe smp 1 -cwd -t 1:$ensnum model.sh $workdir $outdir"
	ssh $SGE_O_HOST "cd $SGE_O_WORKDIR/../Code && qsub -N $jobname -l cpu_arch=skylake_silver -e /dev/null -o /dev/null -q all.q -l h_vmem=6G -pe smp 1 -cwd -t 1:$ensnum model.sh $workdir $outdir"
fi
