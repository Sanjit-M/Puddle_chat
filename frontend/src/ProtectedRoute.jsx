import { Navigate } from "react-router-dom"
import { useEffect, useState } from "react"
import axios from "axios"

export default function ProtectedRoute({ children }) {
	const [isAuthenticated, setIsAuthenticated] = useState(null)

	useEffect(() => {
		axios
			.get("http://localhost:6969/check-auth", { withCredentials: true })
			.then(res => setIsAuthenticated(true))
			.catch(() => setIsAuthenticated(false))
	}, [])

	if (isAuthenticated === null)
		return (
			<div className="flex items-center justify-center h-screen">
				<p className="font-medium">Loading...</p>
			</div>
		)

	return isAuthenticated ? children : <Navigate to="/login" />
}
