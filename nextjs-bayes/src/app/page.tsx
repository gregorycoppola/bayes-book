'use client';

import { useState } from 'react';
import GraphViewer from '@/components/GraphViewer';

export default function Home() {
  const [name, setName] = useState('');
  const [submittedName, setSubmittedName] = useState<string | null>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (name.trim()) {
      setSubmittedName(name.trim());
    }
  };

  return (
    <div className="min-h-screen bg-black text-white flex flex-col items-center p-8 gap-8">
      <h1 className="text-3xl font-bold">Bayesian Network Viewer</h1>

      <form onSubmit={handleSubmit} className="flex gap-4 items-center">
        <input
          type="text"
          placeholder="Enter network name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="bg-white text-black px-4 py-2 rounded-md w-64"
        />
        <button
          type="submit"
          className="bg-blue-600 px-4 py-2 rounded-md hover:bg-blue-500 transition"
        >
          Load Graph
        </button>
      </form>

      {submittedName && (
        <div className="w-full max-w-4xl h-[600px]">
          <GraphViewer name={submittedName} />
        </div>
      )}
    </div>
  );
}
