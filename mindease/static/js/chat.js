document.addEventListener("DOMContentLoaded", () => {
    const chatForm = document.getElementById("chat-form");
    const chatInput = document.getElementById("chat-input");
    const chatBox = document.getElementById("chat-box");
    const emergencyBox = document.getElementById("emergency-box");

    const scrollToBottom = () => {
        chatBox.scrollTop = chatBox.scrollHeight;
    };

    const createBubble = (text, className, timestamp) => {
        const wrapper = document.createElement("div");
        wrapper.className = `bubble ${className}`;

        const content = document.createElement("p");
        content.textContent = text;

        const timeElement = document.createElement("span");
        timeElement.textContent = timestamp;

        wrapper.appendChild(content);
        wrapper.appendChild(timeElement);

        return wrapper;
    };

    if (!chatForm || !chatInput || !chatBox || !window.MINDEASE_CHAT_SEND_URL) {
        return;
    }

    scrollToBottom();

    chatForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const message = chatInput.value.trim();
        if (!message) {
            return;
        }

        const timestamp = new Date().toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
        });

        const userBubble = createBubble(message, "user-bubble", timestamp);
        chatBox.appendChild(userBubble);
        scrollToBottom();

        chatInput.value = "";
        chatInput.focus();

        try {
            const response = await fetch(window.MINDEASE_CHAT_SEND_URL, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ message }),
            });

            if (!response.ok) {
                throw new Error("Failed to send message");
            }

            const data = await response.json();
            const botBubble = createBubble(data.bot_reply, "bot-bubble", data.created_at);
            chatBox.appendChild(botBubble);

            if (data.emergency_prompt && emergencyBox) {
                emergencyBox.classList.remove("hidden");
            }
        } catch (error) {
            const failBubble = createBubble(
                "I hit a temporary issue while replying. Please try again.",
                "bot-bubble",
                timestamp
            );
            chatBox.appendChild(failBubble);
        }

        scrollToBottom();
    });
});
