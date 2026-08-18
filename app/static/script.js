console.log("SCRIPT.JS LOADED");



const askButton = document.getElementById("ask-btn");
const queryInput = document.getElementById("query");
const answerDiv = document.getElementById("answer");
const sourcesList = document.getElementById("sources");
const fileInput = document.getElementById("file-input");
const uploadButton = document.getElementById("upload-btn");
console.log("Upload button:", uploadButton);
const uploadStatus = document.getElementById("upload-status");
const deleteButton = document.getElementById("delete-btn");

// Improvement 1: Allow Enter key to trigger the search
queryInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        askButton.click();
    }
});
uploadButton.addEventListener("click", () => {
    console.log("UPLOAD BUTTON CLICKED");
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


//upload function 
uploadButton.addEventListener("click", async () => {

    const file = fileInput.files[0];

    if (!file) {
        uploadStatus.textContent = "Please select a PDF.";
        return;
    }

    uploadButton.disabled = true;
    uploadButton.textContent = "Uploading...";
    uploadStatus.textContent = "Uploading document...";

    const formData = new FormData();
    formData.append("file", file);

    try {

        const response = await fetch("/upload", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || "Upload failed."
            );
        }

        uploadStatus.textContent =
            `✅ ${data.filename} uploaded successfully. ${data.chunks} chunks indexed.`;

        fileInput.value = "";

    } catch (error) {

        uploadStatus.textContent =
            `❌ ${error.message}`;

        console.error("Upload error:", error);

    } finally {

        uploadButton.disabled = false;
        uploadButton.textContent = "Upload PDF";

    }

});

//delete function 

deleteButton.addEventListener("click", async () => {

    const confirmed = confirm(
        "Are you sure you want to delete the current knowledge base?"
    );

    if (!confirmed) {
        return;
    }

    deleteButton.disabled = true;
    deleteButton.textContent = "Deleting...";

    try {

        const response = await fetch("/collection", {
            method: "DELETE"
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Delete failed.");
        }

        uploadStatus.textContent = "🗑️ Knowledge base cleared.";

        answerDiv.textContent =
            "Upload a PDF to start asking questions.";

        sourcesList.innerHTML = "";

        fileInput.value = "";

    } catch (error) {

        uploadStatus.textContent =
            `❌ ${error.message}`;

        console.error(error);

    } finally {

        deleteButton.disabled = false;
        deleteButton.textContent = "🗑 Clear Documents";

    }

});