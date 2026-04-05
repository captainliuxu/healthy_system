export async function sendChatMessage(text) {
  const res = await fetch(`/api/chat?msg=${encodeURIComponent(text)}`)
  return await res.json()
}