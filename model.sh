export OMPI_MCA_oob=^usock
num=$(($SGE_TASK_ID - 1))
workdir=$1
outdir=$2
mkdir -p $workdir
cp $outdir/$num.* $workdir/.
asynch $workdir/$num.gbl
rm $workdir/$num.str
rm $workdir/$num.gbl
rm $workdir/$num.ini 
sed -i '1 d' "$workdir/`printf %04d $num`.csv"
sed -i '1 d' "$workdir/`printf %04d $num`.csv"
sed -i '1 d' "$workdir/`printf %04d $num`.csv"
mv $workdir/`printf %04d $num`.csv $outdir/output/`printf %04d $num`.csv
