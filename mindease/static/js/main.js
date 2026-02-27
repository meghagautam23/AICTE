document.addEventListener("DOMContentLoaded", () => {
    const sidebar = document.getElementById("sidebar");
    const menuToggle = document.getElementById("menu-toggle");

    if (menuToggle && sidebar) {
        menuToggle.addEventListener("click", () => {
            sidebar.classList.toggle("open");
        });
    }

    const quoteButton = document.getElementById("quote-btn");
    const quoteText = document.getElementById("quote-text");

    if (quoteButton && quoteText && window.MINDEASE_QUOTE_URL) {
        quoteButton.addEventListener("click", async () => {
            quoteButton.disabled = true;
            quoteButton.textContent = "Loading...";
            try {
                const response = await fetch(window.MINDEASE_QUOTE_URL);
                if (!response.ok) {
                    throw new Error("Unable to fetch quote");
                }
                const data = await response.json();
                quoteText.textContent = data.quote;
            } catch (error) {
                quoteText.textContent = "You are still moving forward, even on a difficult day.";
            } finally {
                quoteButton.disabled = false;
                quoteButton.textContent = "Generate New Quote";
            }
        });
    }
});
