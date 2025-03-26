document.addEventListener("DOMContentLoaded", function () {
    const chatBox = document.getElementById("chatBox");
    const userMessageInput = document.getElementById("userMessage");

    function addMessageToChat(sender, message) {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add(sender);
        messageDiv.innerHTML = `<strong>${sender}:</strong> ${message}`;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to latest message
    }

    function queryDocument() {
        const userMessage = userMessageInput.value.trim();
        if (!userMessage) return;

        // Add user message to chat
        addMessageToChat("User", userMessage);
        userMessageInput.value = ""; // Clear input field

        fetch("http://localhost:8000/query-page/", {
            method: "POST",
            headers: {  
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken(),
            },
            body: JSON.stringify({ message: userMessage }),
        })
        .then(response => response.json())
        .then(data => {
            const botResponse = data.response.length ? data.response.join("\n") : "Sorry, no relevant document found.";
            addMessageToChat("Chatbot", botResponse);
        })
        .catch(error => {
            console.error("Error:", error);
            addMessageToChat("Chatbot", "Something went wrong. Please try again.");
        });
    }

    function getCSRFToken() {
        return document.cookie.split("; ")
            .find(row => row.startsWith("csrftoken"))
            ?.split("=")[1] || "";
    }

    // ✅ Detect Enter Key Press & Submit
    userMessageInput.addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();  // Prevent default form submission
            queryDocument();  // Call the function to send the message
        }
    });

    // ✅ Allow button click to submit as well
    document.querySelector("button").addEventListener("click", queryDocument);
});
