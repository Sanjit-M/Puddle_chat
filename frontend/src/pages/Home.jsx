import React from "react"
import { useNavigate } from "react-router-dom"

export default function Home() {
	const navigate = useNavigate()

	return (
		<div className="flex items-center justify-center h-screen flex-col gap-4">
			<h1 className="text-4xl font-bold">Puddle</h1>

			<div className="flex items-center justify-center gap-4">
				<a
					onClick={() => navigate("/login")}
					className="border border-neutral-400 text-neutral-700 hover:border-black hover:text-black transition-colors duration-150 px-4 py-1 rounded-md cursor-pointer"
				>
					Log In
				</a>
				<a
					onClick={() => navigate("/signup")}
					className="border border-neutral-400 text-neutral-700 hover:border-black hover:text-black transition-colors duration-150 px-4 py-1 rounded-md cursor-pointer"
				>
					Sign Up
				</a>
			</div>
		</div>
	)
}
