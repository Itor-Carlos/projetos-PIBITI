"use client";

import { useState } from "react";
import axios from "axios";

export default function Calculadora() {
  const [expressao, setExpressao] = useState("");
  const [resultado, setResultado] = useState(null);
  const [loading, setLoading] = useState(false);

  const calcular = async () => {
    if (!expressao) return;
    setLoading(true);
    try {
      const res = await axios.post("http://localhost:8000/generate", {
        prompt: expressao,
      });
      setResultado(res.data.response);
    } catch (err) {
      setResultado("Erro ao calcular.");
    }
    setLoading(false);
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-blue-500 via-indigo-600 to-purple-700 p-4">
      <div className="backdrop-blur-lg bg-white/20 border border-white/30 shadow-xl rounded-2xl p-8 w-full max-w-md text-white">
        <h1 className="text-3xl font-extrabold mb-6 text-center drop-shadow-md">
          Calculadora Científica IA
        </h1>

        <input
          type="text"
          value={expressao}
          onChange={(e) => setExpressao(e.target.value)}
          placeholder="Digite a expressão (ex: 2+2*3)"
          className="w-full p-3 mb-5 rounded-xl border border-white/30 bg-white/10 text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-yellow-300"
        />

        <button
          onClick={calcular}
          disabled={loading}
          className="w-full py-3 rounded-xl font-semibold bg-gradient-to-r from-yellow-400 via-orange-500 to-pink-500 hover:from-yellow-500 hover:via-orange-600 hover:to-pink-600 transition-all shadow-lg disabled:opacity-60"
        >
          {loading ? "Calculando..." : "Calcular"}
        </button>

        {resultado && (
          <div className="mt-6 text-center">
            <span className="inline-block bg-white/20 border border-white/40 px-4 py-2 rounded-lg text-lg font-medium shadow-sm">
              <span className="font-bold">Resultado:</span> {resultado}
            </span>
          </div>
        )}
      </div>
    </div>
  );
}
