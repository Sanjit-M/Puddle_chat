import React from "react"
import { useState, useEffect, useRef } from "react"
import axios from "axios"

export default function Chat() {
	axios.defaults.withCredentials = true

	const [messages, setMessages] = useState([])
	const [input, setInput] = useState("")
	const [loading, setLoading] = useState(false)
	const messagesEndRef = useRef(null)

	const fetchMessages = async () => {
		try {
			const res = await axios.get(
				"http://localhost:5000/get_conversation"
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
			const res = await axios.post("http://localhost:5000/send_message", {
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
			await axios.post("http://localhost:5000/clear_history")
			setMessages([])
		} catch (err) {
			console.error("Failed to clear chat:", err)
		}
	}

	return (
		<div>
			<h2 className="text-2xl font-bold">Puddle</h2>
			<a className="border border-neutral-400 text-neutral-700 hover:border-black hover:text-black transition-colors duration-150 px-4 py-1 rounded-md cursor-pointer">
				Clear chat
			</a>
			<a className="border border-red-600 text-red-600 hover:border-red-500 hover:text-red-500 transition-colors duration-150 px-4 py-1 rounded-md cursor-pointer">
				Log out
			</a>

			<div>
				<div>
					{messages.map((msg, idx) => (
						<div key={idx}>
							<strong>
								{msg.sender === "user" ? "You" : "Assistant"}:
							</strong>{" "}
							{msg.content}
						</div>
					))}
					<div ref={messagesEndRef} />
				</div>

				<div>
					<textarea
						rows={2}
						value={input}
						onChange={e => setInput(e.target.value)}
						onKeyDown={handleKeyPress}
						placeholder="Type your message..."
					/>
					<button onClick={sendMessage} disabled={loading}>
						Send
					</button>
					<button onClick={clearChat}>Clear Chat</button>
				</div>
			</div>
		</div>
	)
}
