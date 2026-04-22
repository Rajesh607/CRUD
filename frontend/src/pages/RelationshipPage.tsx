import { FormEvent, useState } from "react";
import client from "../api/client";
import { Relationship } from "../types";

export default function RelationshipPage() {
  const [companyAId, setCompanyAId] = useState("");
  const [targetId, setTargetId] = useState("");
  const [result, setResult] = useState<Relationship | null>(null);

  const onAnalyze = async (e: FormEvent) => {
    e.preventDefault();
    const res = await client.post("/analyze", {
      company_a_id: Number(companyAId),
      target_company_id: Number(targetId),
    });
    setResult(res.data);
  };

  return (
    <div className="space-y-4">
      <form onSubmit={onAnalyze} className="bg-white p-6 rounded shadow space-y-3">
        <h2 className="text-2xl font-semibold">Relationship Analysis</h2>
        <input className="border p-2 w-full" placeholder="Company A ID" value={companyAId} onChange={(e) => setCompanyAId(e.target.value)} />
        <input className="border p-2 w-full" placeholder="Target Company ID" value={targetId} onChange={(e) => setTargetId(e.target.value)} />
        <button className="bg-slate-900 text-white px-4 py-2 rounded">Analyze</button>
      </form>
      {result && (
        <div className="bg-white p-6 rounded shadow">
          <p><b>Similarity:</b> {result.similarity_score}</p>
          <p><b>Risk:</b> {result.risk_score}</p>
          <p><b>Opportunity:</b> {result.opportunity_score}</p>
          <p><b>Confidence:</b> {result.confidence_score}</p>
          <p className="mt-2">{result.ai_summary}</p>
        </div>
      )}
    </div>
  );
}
