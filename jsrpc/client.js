let socket;

function connect() {
    socket = new WebSocket("ws://localhost:8080/ws?id=echo");

    socket.onopen = () => {
        console.log("Connected to server");
    };

    socket.onmessage = (event) => {
        console.log("Received from server:", event.data);
        socket.send(event.data); // echo 回发
    };

    socket.onerror = (error) => {
        console.error("WebSocket error:", error);
        socket.close(); // 主动关闭，触发 onclose
    };

    socket.onclose = () => {
        console.warn("WebSocket closed. Reconnecting...");
        setTimeout(connect, 1000);
    };
}

connect();
