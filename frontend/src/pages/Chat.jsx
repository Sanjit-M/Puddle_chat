import React from "react"
import { useState, useEffect, useRef } from "react"
import axios from "axios"
import { useNavigate } from "react-router-dom"

export default function Chat() {
	const navigate = useNavigate()

	axios.defaults.withCredentials = true

	const [messages, setMessages] = useState([])
	const [input, setInput] = useState("")
	const [loading, setLoading] = useState(false)
	const messagesEndRef = useRef(null)

	async function fetchMessages() {
		try {
			const res = await axios.get(
				"http://localhost:6969/get_conversation"
			)
			setMessages(res.data.messages)
		} catch (err) {
			console.error("Failed to load messages:", err)
		}
	}

	useEffect(() => {
		fetchMessages()
	}, [])

	useEffect(() => {
		messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
	}, [messages])

	const sendMessage = async () => {
		if (!input.trim()) return

		const userMessage = {
			sender: "user",
			content: input,
			timestamp: new Date().toISOString(),
		}
		setMessages(prev => [...prev, userMessage])
		setInput("")
		setLoading(true)

		try {
			const res = await axios.post("http://localhost:6969/send_message", {
				content: input,
			})
			const llmMessage = {
				sender: "llm",
				content: res.data.response,
				timestamp: new Date().toISOString(),
			}
			setMessages(prev => [...prev, llmMessage])
		} catch (err) {
			const errorMsg = {
				sender: "llm",
				content: "Error: Failed to get response from server.",
				timestamp: new Date().toISOString(),
			}
			setMessages(prev => [...prev, errorMsg])
		} finally {
			setLoading(false)
		}
	}

	const handleKeyPress = e => {
		if (e.key === "Enter" && !e.shiftKey) {
			e.preventDefault()
			sendMessage()
		}
	}

	const clearChat = async () => {
		try {
			await axios.post("http://localhost:6969/clear_history")
			setMessages([])
		} catch (err) {
			console.error("Failed to clear chat:", err)
		}
	}

	async function logOut() {
		try {
			await axios.get("http://localhost:6969/logout")
			navigate("/")
		} catch (err) {
			console.error("Failed to log out:", err)
		}
	}

	return (
		<div className="w-[45rem] pt-4 mx-auto">
			<div className="flex items-center justify-between pb-2 border-b-2">
				<h2 className="text-2xl font-bold">Puddle</h2>

				<div className="flex items-center gap-4">
					<a
						onClick={clearChat}
						className="border border-neutral-400 text-neutral-700 hover:border-black hover:text-black transition-colors duration-150 px-4 py-1 rounded-md cursor-pointer"
					>
						Clear chat
					</a>
					<a
						onClick={logOut}
						className="border border-red-500 text-red-500 hover:border-red-700 hover:text-red-700 transition-colors duration-150 px-4 py-1 rounded-md cursor-pointer"
					>
						Log out
					</a>
				</div>
			</div>

			<div className="mt-4">
				<div className="flex flex-col gap-3">
					{messages.length <= 0 && (
						<p className="self-center text-neutral-500">
							Ask anything to get started
						</p>
					)}
					{messages.map((msg, idx) => (
						<p
							key={idx}
							className={`px-4 py-2 rounded-md ${
								msg.sender === "user"
									? "self-end bg-blue-100"
									: "self-start bg-neutral-100"
							}`}
						>
							{msg.content}
						</p>
					))}
					{loading && <p className="text-neutral-500">Thinking...</p>}
					<div ref={messagesEndRef} />
				</div>

				<div className="mt-1 flex gap-2 items-center justify-center mb-4">
					<input
						type="text"
						className="border-2 border-neutral-400 rounded-md px-4 py-1 focus:outline-none focus:border-black grow"
						value={input}
						onChange={e => setInput(e.target.value)}
						onKeyDown={handleKeyPress}
						placeholder="Type your message"
					/>
					<button
						onClick={sendMessage}
						disabled={loading || input.length <= 0}
						className={`${
							loading || input.length <= 0
								? "border border-neutral-200 text-neutral-200 px-4 py-1 rounded-md cursor-not-allowed"
								: "border border-neutral-400 text-neutral-700 hover:border-black hover:text-black transition-colors duration-150 px-4 py-1 rounded-md cursor-pointer"
						}`}
					>
						Send
					</button>
				</div>
			</div>
		</div>
	)
}
