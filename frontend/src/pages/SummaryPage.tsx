import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import client from "../api/client";
import { Summary } from "../types";

export default function SummaryPage() {
  const { companyId } = useParams();
  const [summary, setSummary] = useState<Summary | null>(null);

  useEffect(() => {
    client.get(`/summary/${companyId}`).then((res) => setSummary(res.data));
  }, [companyId]);

  if (!summary) return <p>Loading summary...</p>;

  return (
    <div className="bg-white p-6 rounded shadow space-y-3">
      <h2 className="text-2xl font-semibold">Company Summary</h2>
      <p>{summary.overview}</p>
      <section><h3 className="font-semibold">Key insights</h3><ul className="list-disc pl-5">{summary.key_insights.map((i) => <li key={i}>{i}</li>)}</ul></section>
      <section><h3 className="font-semibold">Risks</h3><ul className="list-disc pl-5">{summary.risks.map((i) => <li key={i}>{i}</li>)}</ul></section>
      <section><h3 className="font-semibold">Important facts</h3><ul className="list-disc pl-5">{summary.important_facts.map((i) => <li key={i}>{i}</li>)}</ul></section>
    </div>
  );
}
