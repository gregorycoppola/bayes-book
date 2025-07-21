'use client';

import { useEffect, useRef, useState } from 'react';
import { Network } from 'vis-network/standalone/esm/vis-network';
import 'vis-network/styles/vis-network.css';

interface GraphData {
  nodes: { id: string; label: string }[];
  edges: { from: string; to: string }[];
}

interface GraphViewerProps {
  name: string; // Network name to fetch from /networks/{name}/graph
}

export default function GraphViewer({ name }: GraphViewerProps) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchGraph = async () => {
      try {
        const res = await fetch(`/networks/${name}/graph`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data: GraphData = await res.json();
        if (containerRef.current) {
          const options = {
            layout: {
              hierarchical: {
                enabled: true,
                direction: 'UD', // Top-down
                sortMethod: 'directed'
              }
            },
            physics: false,
            nodes: {
              shape: 'box',
              font: { face: 'monospace' }
            },
            edges: {
              arrows: {
                to: { enabled: true }
              }
            }
          };
          new Network(containerRef.current, data, options);
        }
        setLoading(false);
      } catch (err) {
        setError('Failed to load graph');
        console.error(err);
        setLoading(false);
      }
    };

    fetchGraph();
  }, [name]);

  return (
    <div style={{ width: '100%', height: '600px', background: '#111' }}>
      {loading && <p style={{ color: 'white' }}>Loading graph...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <div ref={containerRef} style={{ width: '100%', height: '100%' }} />
    </div>
  );
}
