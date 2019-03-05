echo
python print_keys.py --all > Analyze/result_all
echo
echo "Print all keys"
echo

python print_keys.py --one > Analyze/result_1_1
echo
echo "Print 1:1 keys"
echo

python print_keys.py --overlap > Analyze/result_1_N
echo
echo "Print 1:N keys"
echo
