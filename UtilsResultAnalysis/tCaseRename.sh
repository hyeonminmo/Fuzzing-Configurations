declare -i a=0
for entry in $1/*
do
	cp $entry $2/t_case_$a 
	a=$((a + 1))
done
