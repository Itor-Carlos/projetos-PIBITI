"use client";

import { useState } from "react";

export default function MoviesPage() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const handleAsk = async () => {
    const res = await fetch(`/api/ask?q=${encodeURIComponent(question)}`);
    const data = await res.json();
    setAnswer(data.answer);
  };

  return (
    <div className="p-6 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Movie Chat</h1>
      <input
        className="border p-2 w-full rounded mb-2"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Escreva sua pergunta sobre filmes..."
      />
      <button
        className="bg-green-600 text-white px-4 py-2 rounded"
        onClick={handleAsk}
      >
        Perguntar
      </button>
      {answer && (
        <div className="mt-4 p-4 bg-gray-100 rounded shadow">
          <p><b>Resposta:</b> {answer}</p>
        </div>
      )}
    </div>
  );
}