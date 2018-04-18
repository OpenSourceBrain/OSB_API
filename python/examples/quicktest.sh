set -e

echo "=== CheckModelDB ==="
python CheckModelDB.py 10

echo "=== activity ==="
python activity.py 10

echo "=== curate ==="
python curate.py 10

echo "=== retreiveNML2 ==="
python retrieveNML2.py 16

echo "=== tags ==="
python tags.py

if [ "$1" == "-a" ]; then
    echo "=== project_metadata ==="
    python project_metadata.py
fi
