import { ReactNode, useState } from "react"
import { api } from '../api/client';

type BaseLayoutProps = {
    children: ReactNode;
}

function handleLogOut() {
    const token = localStorage.getItem("token")
    if (!token) {
        return null;
    }
    localStorage.removeItem("token");
    window.location.href = "/"
}

export default function BaseLayout({children}: BaseLayoutProps) {
    
    return (
        <div>
            <header>
                
                <div>
                    <a href="/"><button>Home</button></a>
                    <a href="/custom"><button>Custom Foods</button></a>
                    <a href="/statistics"><button>Statistics</button></a>
                    <button onClick={handleLogOut}>Log Out</button>
                </div>

            </header>
            {children}
        </div>
    )
}