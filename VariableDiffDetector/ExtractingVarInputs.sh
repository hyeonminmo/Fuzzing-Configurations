for entry in $2/*
do
    python3 ExtractingVarInputs.py $1 $entry
done