const token = "这里换成你自己的 access_token";
const ws = new WebSocket(
  `ws://127.0.0.1:8000/api/v1/realtime/ws?token=${token}`
);

ws.onopen = () => {
  console.log("ws connected");
  ws.send("ping");
};

ws.onmessage = (event) => {
  console.log("ws message:", JSON.parse(event.data));
};

ws.onclose = (event) => {
  console.log("ws closed:", event.code, event.reason);
};