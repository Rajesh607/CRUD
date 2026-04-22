import { useEffect, useState } from "react";
import client from "../api/client";

interface Upload {
  id: number;
  filename: string;
  company_type: string;
  status: string;
  created_at: string;
}

export default function HistoryPage() {
  const [uploads, setUploads] = useState<Upload[]>([]);

  useEffect(() => {
    client.get("/uploads").then((res) => setUploads(res.data));
  }, []);

  return (
    <div className="bg-white p-6 rounded shadow">
      <h2 className="text-2xl font-semibold mb-4">Upload History</h2>
      <table className="w-full border-collapse">
        <thead>
          <tr className="border-b">
            <th className="text-left p-2">ID</th>
            <th className="text-left p-2">File</th>
            <th className="text-left p-2">Type</th>
            <th className="text-left p-2">Status</th>
          </tr>
        </thead>
        <tbody>
          {uploads.map((upload) => (
            <tr key={upload.id} className="border-b">
              <td className="p-2">{upload.id}</td>
              <td className="p-2">{upload.filename}</td>
              <td className="p-2">{upload.company_type}</td>
              <td className="p-2">{upload.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
