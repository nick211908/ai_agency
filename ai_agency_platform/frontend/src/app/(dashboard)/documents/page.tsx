export default function DocumentsPage() {
    return (
        <div className="space-y-4">
            <h1 className="text-3xl font-bold text-gray-900">Documents</h1>
            <p className="text-gray-600">
                Upload and manage legal source documents from the Legal Agency workspace.
            </p>
            <div className="rounded-xl border border-dashed border-gray-300 bg-white p-6 text-sm text-gray-500">
                Select <span className="font-medium text-gray-700">Legal Agency</span> in Dashboard and use the file upload control to ingest documents.
            </div>
        </div>
    );
}
