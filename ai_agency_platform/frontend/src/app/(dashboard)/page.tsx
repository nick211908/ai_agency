"use client";

import { useState } from "react";
import { api } from "@/lib/api";
import { Send, Upload, FileUp, Briefcase, PenTool } from "lucide-react";

export default function Dashboard() {
    const [selectedAgency, setSelectedAgency] = useState<"legal" | "design" | null>(null);
    const [prompt, setPrompt] = useState("");
    const [messages, setMessages] = useState<{ role: string, content: string }[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    const [file, setFile] = useState<File | null>(null);

    const handleRunAgency = async () => {
        if (!prompt || !selectedAgency) return;

        setIsLoading(true);
        setMessages(prev => [...prev, { role: "user", content: prompt }]);
        setPrompt("");

        try {
            const res = await api.agency.run(prompt, selectedAgency);
            const data = res.data;

            if (data.status === "success") {
                let outputMsg = "";
                if (selectedAgency === "legal") {
                    // Prioritize structured output (document + metrics)
                    if (data.output && data.output.document) {
                        outputMsg = "";

                        // Add Metrics if available
                        if (data.metrics) {
                            const riskScore = data.metrics.risk_score || "N/A";
                            outputMsg += `**Risk Score:** ${riskScore}/100\n\n`;
                        }

                        // Add the main document content
                        outputMsg += data.output.document;
                    } else {
                        // Fallback to simpler output or messages
                        outputMsg = typeof data.output === 'string' ? data.output : JSON.stringify(data.output.output || data.output, null, 2);

                        // If messages list exists and we didn't get a document, try to grab the last AI message
                        // But ONLY if we haven't already found a document
                        if (!outputMsg || outputMsg === "{}" || outputMsg === "[]") {
                            if (data.messages && data.messages.length > 0) {
                                outputMsg = data.messages[data.messages.length - 1];
                            }
                        }
                    }
                } else {
                    // Design output structure might be different
                    outputMsg = JSON.stringify(data.output, null, 2);
                    // Check for artifact url
                    if (data.output?.artifacts?.image?.url) {
                        outputMsg = `Generated Image: ${data.output.artifacts.image.url}\n\n` + outputMsg;
                    }
                }
                setMessages(prev => [...prev, { role: "assistant", content: outputMsg }]);
            } else {
                setMessages(prev => [...prev, { role: "assistant", content: "Error running agency." }]);
            }
        } catch (error) {
            setMessages(prev => [...prev, { role: "assistant", content: "Request failed." }]);
            console.error(error);
        } finally {
            setIsLoading(false);
        }
    };

    const handleUpload = async () => {
        if (!file) return;
        try {
            await api.agency.ingest(file);
            alert("Fileingested successfully!");
            setFile(null);
        } catch (e) {
            alert("Upload failed");
        }
    };

    return (
        <div className="max-w-6xl mx-auto space-y-8">

            {/* Header */}
            <div>
                <h1 className="text-3xl font-bold text-gray-900">Agency Command Center</h1>
                <p className="text-gray-500 mt-2">Select an autonomous agency to start working.</p>
            </div>

            {/* Agency Selector */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div
                    onClick={() => setSelectedAgency("legal")}
                    className={`p-6 bg-white rounded-xl shadow-sm border-2 cursor-pointer transition-all ${selectedAgency === "legal" ? "border-indigo-600 bg-indigo-50" : "border-transparent hover:border-gray-200"}`}
                >
                    <div className="flex items-center space-x-4">
                        <div className="p-3 bg-blue-100 text-blue-600 rounded-lg">
                            <Briefcase className="w-8 h-8" />
                        </div>
                        <div>
                            <h3 className="text-xl font-semibold text-gray-900">Legal Agency</h3>
                            <p className="text-gray-500">Contract drafting, research, and compliance reviews.</p>
                        </div>
                    </div>
                </div>

                <div
                    onClick={() => setSelectedAgency("design")}
                    className={`p-6 bg-white rounded-xl shadow-sm border-2 cursor-pointer transition-all ${selectedAgency === "design" ? "border-pink-600 bg-pink-50" : "border-transparent hover:border-gray-200"}`}
                >
                    <div className="flex items-center space-x-4">
                        <div className="p-3 bg-pink-100 text-pink-600 rounded-lg">
                            <PenTool className="w-8 h-8" />
                        </div>
                        <div>
                            <h3 className="text-xl font-semibold text-gray-900">Design Agency</h3>
                            <p className="text-gray-500">Visual concepts, copywriting, and creative direction.</p>
                        </div>
                    </div>
                </div>
            </div>

            {/* Workspace */}
            {selectedAgency && (
                <div className="bg-white rounded-xl shadow-md overflow-hidden min-h-[500px] flex flex-col">
                    {/* Toolbar */}
                    <div className="p-4 border-b bg-gray-50 flex justify-between items-center">
                        <h2 className="font-semibold text-gray-700 flex items-center capitalize">
                            {selectedAgency === 'legal' ? <Briefcase className="w-4 h-4 mr-2" /> : <PenTool className="w-4 h-4 mr-2" />}
                            {selectedAgency} Agency Workspace
                        </h2>
                        {selectedAgency === 'legal' && (
                            <div className="flex items-center space-x-2">
                                <input
                                    type="file"
                                    onChange={(e) => setFile(e.target.files?.[0] || null)}
                                    className="text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100"
                                />
                                <button
                                    onClick={handleUpload}
                                    disabled={!file}
                                    className="p-2 text-gray-600 hover:text-indigo-600 disabled:opacity-50"
                                    title="Ingest Document"
                                >
                                    <Upload className="w-5 h-5" />
                                </button>
                            </div>
                        )}
                    </div>

                    {/* Chat Area */}
                    <div className="flex-1 p-6 space-y-4 overflow-y-auto max-h-[600px] bg-gray-50">
                        {messages.length === 0 && (
                            <div className="text-center text-gray-400 mt-20">
                                <p>Start a task by typing below.</p>
                            </div>
                        )}
                        {messages.map((msg, idx) => (
                            <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                                <div className={`max-w-[80%] rounded-lg p-4 ${msg.role === 'user' ? 'bg-indigo-600 text-white' : 'bg-white shadow-sm border text-gray-800'}`}>
                                    <pre className="whitespace-pre-wrap font-sans text-sm">{msg.content}</pre>
                                </div>
                            </div>
                        ))}
                        {isLoading && (
                            <div className="flex justify-start">
                                <div className="bg-white shadow-sm border text-gray-800 rounded-lg p-4">
                                    <span className="animate-pulse">Thinking...</span>
                                </div>
                            </div>
                        )}
                    </div>

                    {/* Input Area */}
                    <div className="p-4 border-t bg-white">
                        <div className="flex space-x-2">
                            <textarea
                                value={prompt}
                                onChange={(e) => setPrompt(e.target.value)}
                                placeholder={`Ask the ${selectedAgency} agency to do something...`}
                                className="flex-1 p-3 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none"
                                rows={2}
                                onKeyDown={(e) => {
                                    if (e.key === 'Enter' && !e.shiftKey) {
                                        e.preventDefault();
                                        handleRunAgency();
                                    }
                                }}
                            />
                            <button
                                onClick={handleRunAgency}
                                disabled={isLoading || !prompt.trim()}
                                className="px-6 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
                            >
                                <Send className="w-5 h-5" />
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}
