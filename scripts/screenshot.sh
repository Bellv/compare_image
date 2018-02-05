for x in `cat site.txt`
do
  node scripts/index.js $1 $x $2
done
