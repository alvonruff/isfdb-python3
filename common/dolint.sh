
# Generate the list of Python files

python_files=$(find . -maxdepth 1 -name "*.py")
touch LOG

# Copy the pylintrc file here if necessary

current_dir=$(basename "$(pwd)")
if [ "$current_dir" != "common" ]; then
    echo "Making local copy of pylintrc file"
    cp ../common/pylintrc .
fi

#
# Run pylint on each file
#
echo "Running pylint on each python file:"
for file in $python_files; do
    echo $file
    pylint $file >> LOG
done
cat LOG

#
# Check for these errors
#
echo "======================================================="
echo "          Important Errors"
echo "======================================================="
touch ERRORS
grep "unexpected indent" LOG >> ERRORS
grep "Trailing whitespace" LOG >> ERRORS
grep "Unused" LOG >> ERRORS
grep "exception" LOG >> ERRORS
grep "Redefining" LOG >> ERRORS
sort ERRORS

# Cleanup
rm -f LOG
rm -f ERRORS
current_dir=$(basename "$(pwd)")
if [ "$current_dir" != "common" ]; then
    rm pylintrc
fi


exit 0
