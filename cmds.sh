echo "--- A4 ---"
cat .env.example

echo "--- C2 ---"
find ./results -name "*.csv" 2>/dev/null | sed 's/.*\///;s/\.csv$//' | sort

echo "--- E4 ---"
git ls-files | grep -i "local only"

echo "--- E5 ---"
git log --all --full-history -- "**/.env" 2>/dev/null | head -20

echo "--- F1 ---"
cat requirements.txt
