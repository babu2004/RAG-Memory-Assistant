const askButton = document.getElementById("ask-btn");
const queryInput = document.getElementById("query");
const answerDiv = document.getElementById("answer");
const sourcesList = document.getElementById("sources");

// Improvement 1: Allow Enter key to trigger the search
queryInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        askButton.click();
    }
});

askButton.addEventListener("click", async () => {
    const query = queryInput.value.trim();

    if (!query) {
        alert("Please enter a question.");
        return;
    }

    // Improvement 2: Disable button and change text to prevent spam
    askButton.disabled = true;
    askButton.textContent = "Thinking...";
    answerDiv.textContent = "Thinking...";
    sourcesList.innerHTML = "";

    try {
        const response = await fetch("/query", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ query: query })
        });

        const data = await response.json();
        answerDiv.textContent = data.answer;

        data.sources.forEach(source => {
            const li = document.createElement("li");
            li.textContent = "📄 " + source;
            sourcesList.appendChild(li);
        });
    } catch (error) {
        answerDiv.textContent = "Something went wrong.";
        console.error(error);
    } finally {
        // Improvement 2: Re-enable the button regardless of success or failure
        askButton.disabled = false;
        askButton.textContent = "Ask";
    }
});
