import React from "react"
import { useNavigate } from "react-router-dom"

export default function NotFound() {
	const naviagate = useNavigate()

	function navigateToHome() {
		naviagate("/")
	}

	return (
		<div className="flex flex-col h-screen items-center justify-center gap-4">
			<h1 className="text-4xl font-bold">Page not found</h1>
			<a
				className="text-blue-500 cursor-pointer hover:underline"
				onClick={navigateToHome}
			>
				Go to home
			</a>
		</div>
	)
}
