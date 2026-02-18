"use client";

import { useAuth } from "@/context/auth-context";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import Link from "next/link";
import { LayoutDashboard, FileText, Settings, LogOut } from "lucide-react";

export default function DashboardLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    const { user, loading, logout } = useAuth();
    const router = useRouter();

    useEffect(() => {
        if (!loading && !user) {
            router.push("/login");
        }
    }, [user, loading, router]);

    if (loading) {
        return <div className="flex h-screen items-center justify-center">Loading...</div>;
    }

    if (!user) return null;

    return (
        <div className="flex h-screen bg-gray-100">
            {/* Sidebar */}
            <aside className="w-64 bg-white shadow-md flex flex-col">
                <div className="p-6 border-b">
                    <h1 className="text-2xl font-bold text-indigo-600">AI Agency</h1>
                </div>
                <nav className="flex-1 p-4 space-y-2">
                    <Link href="/" className="flex items-center p-3 text-gray-700 hover:bg-indigo-50 hover:text-indigo-600 rounded-md transition-colors">
                        <LayoutDashboard className="w-5 h-5 mr-3" />
                        Dashboard
                    </Link>
                    <Link href="/documents" className="flex items-center p-3 text-gray-700 hover:bg-indigo-50 hover:text-indigo-600 rounded-md transition-colors">
                        <FileText className="w-5 h-5 mr-3" />
                        Documents
                    </Link>
                    <Link href="/settings" className="flex items-center p-3 text-gray-700 hover:bg-indigo-50 hover:text-indigo-600 rounded-md transition-colors">
                        <Settings className="w-5 h-5 mr-3" />
                        Settings
                    </Link>
                </nav>
                <div className="p-4 border-t">
                    <div className="flex items-center p-3 mb-2">
                        <div className="w-8 h-8 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-600 font-bold mr-3">
                            {user.email[0].toUpperCase()}
                        </div>
                        <div className="text-sm font-medium truncate">{user.email}</div>
                    </div>
                    <button
                        onClick={logout}
                        className="flex items-center w-full p-3 text-red-600 hover:bg-red-50 rounded-md transition-colors"
                    >
                        <LogOut className="w-5 h-5 mr-3" />
                        Sign Out
                    </button>
                </div>
            </aside>

            {/* Main Content */}
            <main className="flex-1 overflow-auto p-8">
                {children}
            </main>
        </div>
    );
}
