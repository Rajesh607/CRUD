export default function DashboardPage() {
  return (
    <div className="space-y-4">
      <h1 className="text-3xl font-bold">BI Dashboard</h1>
      <p>Upload both companies, monitor processing status, and run relationship analysis.</p>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white p-4 rounded shadow">Processing Status</div>
        <div className="bg-white p-4 rounded shadow">Pattern Detection Result</div>
        <div className="bg-white p-4 rounded shadow">Combined Result Overview</div>
      </div>
    </div>
  );
}
