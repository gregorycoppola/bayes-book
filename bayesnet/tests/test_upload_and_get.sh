#!/bin/bash
set -e

echo "🔄 Resetting test environment..."

# Make sure the test file exists
cat > test_network.json <<EOF
{
  "name": "Test Network",
  "nodes": [
    {
      "name": "A",
      "domain": ["true", "false"],
      "parents": [],
      "cpt": {
        "true": [{ "parent_values": {}, "probability": 0.6 }],
        "false": [{ "parent_values": {}, "probability": 0.4 }]
      }
    }
  ]
}
EOF

echo "📤 Uploading network..."
bayes upload testnet test_network.json

echo "📋 Listing networks..."
bayes list

echo "📥 Getting network..."
bayes get testnet

echo "✅ Test completed successfully."
