echo $1
blink-diff --output report/$1 before/$1 after/$1 --verbose --threshold-type percent --threshold $2
