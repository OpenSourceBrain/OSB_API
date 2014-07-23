set -e
if [ "$1" == "-a" ]; then
    python project_metadata.py
fi
echo "=== CheckModelDB ==="
python CheckModelDB.py
echo "=== activity ==="
python activity.py 10
echo "=== curate ==="
python curate.py 10
echo "=== retreiveNML2 ==="
python retrieveNML2.py 20
echo "=== project_metadata ==="
python project_metadata.py 1
echo "=== tags ==="
python tags.py


