import { FormEvent, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import client from "../api/client";

export default function UploadPage() {
  const { companyType } = useParams();
  const navigate = useNavigate();
  const [file, setFile] = useState<File | null>(null);
  const [inputText, setInputText] = useState("");
  const [status, setStatus] = useState("");

  const type = companyType === "target" ? "target_company" : "company_a";

  const submit = async (e: FormEvent) => {
    e.preventDefault();
    const form = new FormData();
    form.append("company_type", type);
    if (file) form.append("file", file);
    if (!file && inputText) form.append("input_text", inputText);

    const response = await client.post("/upload", form, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    setStatus(`Processed: ${response.data.company_name} (${response.data.normalized_by})`);
    navigate(`/summary/${response.data.id}`);
  };

  return (
    <form onSubmit={submit} className="space-y-4 bg-white p-6 rounded shadow">
      <h2 className="text-2xl font-semibold">Upload {type === "company_a" ? "Company A" : "Target Company"}</h2>
      <input type="file" onChange={(e) => setFile(e.target.files?.[0] || null)} className="block" />
      <p className="text-sm text-gray-500">or paste content</p>
      <textarea className="w-full border p-2 h-40" value={inputText} onChange={(e) => setInputText(e.target.value)} />
      <button className="bg-slate-900 text-white px-4 py-2 rounded">Upload & Process</button>
      {status && <p>{status}</p>}
    </form>
  );
}
