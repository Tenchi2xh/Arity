find . -name "*.pyc" -or -name "__pycache__" | xargs rm -rf
rm -rf .cache
rm -rf .benchmarks
rm .coverage