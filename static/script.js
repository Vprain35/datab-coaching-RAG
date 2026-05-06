async function submitQuery() {
    const question = document.getElementById("question").value;
    const collection = document.getElementById("collection").value;
    const responseBox = document.getElementById("responseBox");

    responseBox.innerText = "Loading...";

    try {
        const res = await fetch("http://127.0.0.1:8000/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: question,
                collection: collection
            })
        });

        const data = await res.json();

        // Adjust this depending on your API response format
        responseBox.innerText = data.answer || JSON.stringify(data, null, 2);

    } catch (error) {
        responseBox.innerText = "Error: " + error.message;
    }
}