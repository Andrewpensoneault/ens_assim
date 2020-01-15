export OMPI_MCA_oob=^usock
num=$1
workdir=$2
outdir=$3
mkdir -p $workdir
cp $outdir/$num.* $workdir/.
asynch $workdir/$num.gbl
rm $workdir/$num.gbl
rm $workdir/$num.str
rm $workdir/$num.ini
sed -i '1 d' "$workdir/`printf %04d $num`.csv"
sed -i '1 d' "$workdir/`printf %04d $num`.csv"
sed -i '1 d' "$workdir/`printf %04d $num`.csv"
cp "$workdir/`printf %04d $num`.csv" "$outdir/output/`printf %04d $num`.csv"
rm "$workdir/`printf %04d $num`.csv"
