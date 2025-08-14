N=$1
echo "Running load tests [$1] ..."
DBL_TEST_ENV=1 python3 load_test.py $1