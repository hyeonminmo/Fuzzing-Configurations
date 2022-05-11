declare -i a=0
for entry in $2/*
do
	$1 $entry 2>&1 | grep -a -e '#[0-9]' > $3/stacktrace$a
	a=$((a + 1))
done
