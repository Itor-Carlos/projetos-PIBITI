"use client";
import { useState } from "react";

export default function Calculadora() {
  const [problema, setProblema] = useState("");
  const [resultado, setResultado] = useState(null);
  const [loading, setLoading] = useState(false);

  const calcular = async () => {
    if (!problema.trim()) return;
    
    setLoading(true);
    try {
      const response = await fetch("http://localhost:8000/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          prompt: problema,
        }),
      });
      
      if (response.ok) {
        const data = await response.json();
        setResultado(data.response);
      } else {
        setResultado("Erro ao processar o problema matemático.");
      }
    } catch (err) {
      setResultado("Erro de conexão. Verifique se o servidor está rodando.");
    }
    setLoading(false);
  };

  const limpar = () => {
    setProblema("");
    setResultado(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8 pt-8">
          <h1 className="text-4xl md:text-5xl font-bold text-white mb-4 bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
            🧮 Calculadora Cientifica IA
          </h1>
          <p className="text-gray-300 text-lg">
            Descreva seu problema matemático em linguagem natural e receba uma solução completa com passos detalhados
          </p>
        </div>

        <div className="backdrop-blur-xl bg-white/10 border border-white/20 shadow-2xl rounded-3xl p-6 md:p-8 mb-6">
          <div className="mb-6">
            <label className="block text-white font-semibold mb-3 text-lg">
              Escreva seu problema matemático:
            </label>
            <textarea
              value={problema}
              onChange={(e) => setProblema(e.target.value)}
              placeholder="Ex: Se eu tenho 20 reais e gasto 7 reais no lanche, quanto me sobra? Ou: Calcule a área de um círculo com raio de 5 metros..."
              className="w-full p-4 rounded-2xl border border-white/30 bg-white/10 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent resize-none h-24 text-base"
              rows={3}
            />
          </div>

          {/* Action Buttons */}
          <div className="flex flex-col sm:flex-row gap-3 mb-6">
            <button
              onClick={calcular}
              disabled={loading || !problema.trim()}
              className="flex-1 py-3 px-6 rounded-2xl font-semibold text-white bg-gradient-to-r from-blue-500 via-purple-600 to-pink-600 hover:from-blue-600 hover:via-purple-700 hover:to-pink-700 transition-all duration-300 shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed transform hover:scale-[1.02]"
            >
              {loading ? (
                <span className="flex items-center justify-center">
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Processando...
                </span>
              ) : (
                "Resolução do Problema"
              )}
            </button>
            
            <button
              onClick={limpar}
              className="py-3 px-6 rounded-2xl font-semibold text-white bg-white/20 hover:bg-white/30 transition-all duration-300 border border-white/30 hover:border-white/50"
            >
              Limpar
            </button>
          </div>
        </div>

        {resultado && (
          <div className="backdrop-blur-xl bg-gradient-to-r from-green-900/20 to-blue-900/20 border border-green-400/30 shadow-xl rounded-3xl p-6">
            <h3 className="text-white font-semibold mb-4 text-lg flex items-center">
              Solução em detalhes:
            </h3>
            <div className="bg-white/10 rounded-2xl p-4 border border-white/20">
              <pre className="text-gray-200 whitespace-pre-wrap font-mono text-sm leading-relaxed overflow-x-auto">
                {resultado}
              </pre>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}