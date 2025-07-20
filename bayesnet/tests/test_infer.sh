#!/bin/bash
set -e

echo "🔄 Resetting test environment..."

# Create a simple test network JSON
cat > test_network.json <<EOF
{
  "name": "Inference Test Network",
  "nodes": [
    {
      "name": "A",
      "domain": ["true", "false"],
      "parents": [],
      "cpt": {
        "true": [{ "parent_values": {}, "probability": 0.6 }],
        "false": [{ "parent_values": {}, "probability": 0.4 }]
      }
    },
    {
      "name": "B",
      "domain": ["true", "false"],
      "parents": ["A"],
      "cpt": {
        "true": [
          { "parent_values": { "A": "true" }, "probability": 0.8 },
          { "parent_values": { "A": "false" }, "probability": 0.3 }
        ],
        "false": [
          { "parent_values": { "A": "true" }, "probability": 0.2 },
          { "parent_values": { "A": "false" }, "probability": 0.7 }
        ]
      }
    }
  ]
}
EOF

echo "📤 Uploading network..."
bayes upload infernet test_network.json

echo "📋 Listing networks..."
bayes list

echo "📥 Getting network..."
bayes get infernet

echo "🔍 Running inference with evidence A=true..."
bayes infer infernet --evidence '{"A": "true"}' --iterations 5

echo "✅ Inference test completed successfully."
