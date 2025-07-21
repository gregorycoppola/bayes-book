#!/bin/bash
set -e

echo "🔄 Resetting test environment..."

# Create test network JSON
cat > test_network.json <<EOF
{
  "name": "Graph Test Network",
  "nodes": [
    {
      "name": "X",
      "domain": ["on", "off"],
      "parents": [],
      "cpt": {
        "on": [{ "parent_values": {}, "probability": 0.5 }],
        "off": [{ "parent_values": {}, "probability": 0.5 }]
      }
    },
    {
      "name": "Y",
      "domain": ["on", "off"],
      "parents": ["X"],
      "cpt": {
        "on": [
          { "parent_values": { "X": "on" }, "probability": 0.9 },
          { "parent_values": { "X": "off" }, "probability": 0.2 }
        ],
        "off": [
          { "parent_values": { "X": "on" }, "probability": 0.1 },
          { "parent_values": { "X": "off" }, "probability": 0.8 }
        ]
      }
    }
  ]
}
EOF

echo "📤 Uploading network..."
bayes upload graphtest test_network.json

echo "📋 Listing networks..."
bayes list

echo "📥 Getting network..."
bayes get graphtest

echo "🕸️ Graph structure:"
bayes graph graphtest

echo "✅ Graph test completed successfully."
