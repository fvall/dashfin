# -------------
#  Python app
# ------------

poetry export -f requirements.txt -o requirements.txt

# - Docker

docker rmi finapp || true
docker build -t finapp .

# - Cleanup`

rm requirements.txt