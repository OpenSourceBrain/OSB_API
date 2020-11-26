set -e

echo "=== CheckModelDB ==="
python CheckModelDB.py 5

echo "=== activity ==="
python activity.py 5

echo "=== curate ==="
python curate.py 5

echo "=== retreiveNML2 ==="
python retrieveNML2.py 20

echo "=== tags ==="
python tags.py

if [ "$1" == "-a" ]; then
    echo "=== project_metadata ==="
    python project_metadata.py
fi
