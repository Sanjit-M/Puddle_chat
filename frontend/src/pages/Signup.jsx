import React from "react"
import { useState } from "react"

export default function Signup() {
	const [formData, setFormData] = useState({
		username: "",
		password: "",
		repeatPassword: "",
	})

	function handleChange(e) {
		setFormData({ ...formData, [e.target.name]: e.target.value })
	}

	function handleSubmit(e) {
		e.preventDefault()
		console.log(formData)
	}

	return (
		<div className="flex items-center justify-center h-screen flex-col gap-4">
			<h2 className="text-2xl font-bold">Sign up for Puddle</h2>

			<form
				onSubmit={handleSubmit}
				className="flex items-center justify-center flex-col gap-2"
			>
				<input
					className="border-2 border-neutral-400 rounded-md px-4 py-1"
					type="text"
					name="username"
					placeholder="username"
					onChange={handleChange}
					required
					value={formData.username}
				/>
				<input
					className="border-2 border-neutral-400 rounded-md px-4 py-1"
					type="password"
					name="password"
					placeholder="password"
					onChange={handleChange}
					required
					value={formData.password}
				/>

				<input
					className="border-2 border-neutral-400 rounded-md px-4 py-1"
					type="password"
					name="repeatPassword"
					placeholder="repeat password"
					onChange={handleChange}
					required
					value={formData.repeatPassword}
				/>

				{formData.password.length < 8 && formData.password != "" && (
					<p className="text-red-500">
						password should contain at least 8 characters
					</p>
				)}

				{formData.password != formData.repeatPassword &&
					formData.repeatPassword != "" && (
						<p className="text-red-500">passwords do not match</p>
					)}

				<button
					type="submit"
					className="border border-neutral-400 text-neutral-700 hover:border-black hover:text-black transition-colors duration-150 px-4 py-1 rounded-md cursor-pointer"
				>
					Sign up
				</button>
			</form>
		</div>
	)
}
