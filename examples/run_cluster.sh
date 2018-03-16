# Add raftos package to PYTHONPATH so we don't need to install it to run example
export PYTHONPATH="${PYTHONPATH}:$(pwd)/../"

# Remove previous data
rm -f *.log
rm -f *.storage
rm -f *.state_machine

# Start
python node.py --node "9000" --cluster "9000 9001 9002 9003 9004" &
python node.py --node "9001" --cluster "9000 9001 9002 9003 9004" &
python node.py --node "9002" --cluster "9000 9001 9002 9003 9004" &
python node.py --node "9003" --cluster "9000 9001 9002 9003 9004" &
python node.py --node "9004" --cluster "9000 9001 9002 9003 9004" &

#python node.py --node "9012" --cluster "9012 9013 9014 9015 9016" &
#python node.py --node "9013" --cluster "9012 9013 9014 9015 9016" &
#python node.py --node "9014" --cluster "9012 9013 9014 9015 9016" &
#python node.py --node "9015" --cluster "9012 9013 9014 9015 9016" &
#python node.py --node "9016" --cluster "9012 9013 9014 9015 9016" &

