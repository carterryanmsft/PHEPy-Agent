# Automated Production Report Generator
# Runs Kusto query, converts to CSV, and generates HTML report

Write-Host "`n🔄 Starting automated production report generation..." -ForegroundColor Cyan

# Step 1: Query results are already in memory from the Kusto MCP tool
# We need to re-run the query to get fresh data and save it properly

Write-Host "`n📊 Step 1: Fetching latest data from Kusto..." -ForegroundColor Yellow

# The Python script will need to handle the JSON-to-CSV conversion
# Let me create a Python helper instead since we're already using Python

Write-Host "✓ Switching to Python for JSON-to-CSV conversion" -ForegroundColor Green

# Create the Python conversion script
$pythonScript = @'
import json
import csv
import sys

def convert_kusto_json_to_csv(json_file, csv_file):
    """Convert Kusto query JSON results to CSV format."""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extract the data array
        rows = data.get('data', [])
        
        if not rows:
            print("Error: No data found in JSON file")
            return False
        
        # Write to CSV
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
        
        print(f"✓ Converted {len(rows)} rows to {csv_file}")
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python convert_json_to_csv.py <input.json> <output.csv>")
        sys.exit(1)
    
    convert_kusto_json_to_csv(sys.argv[1], sys.argv[2])
'@

Set-Content -Path 'convert_json_to_csv.py' -Value $pythonScript -Encoding UTF8
Write-Host "✓ Created JSON-to-CSV converter" -ForegroundColor Green

Write-Host "`n📝 Next: Run the Kusto query and save results..." -ForegroundColor Cyan
