document.addEventListener("DOMContentLoaded", () => {
    // Live search filters the cards without making another server request.
    const searchInput = document.getElementById("bookSearch");
    const bookCards = document.querySelectorAll(".book-card");
    const noSearch = document.getElementById("noSearch");

    if (searchInput) {
        searchInput.addEventListener("input", () => {
            const term = searchInput.value.trim().toLowerCase();
            let visibleCount = 0;

            bookCards.forEach((card) => {
                const title = card.dataset.title || "";
                const author = card.dataset.author || "";
                const matches = title.includes(term) || author.includes(term);

                card.style.display = matches ? "" : "none";
                if (matches) visibleCount++;
            });

            if (noSearch) {
                noSearch.hidden = visibleCount !== 0;
            }
        });
    }

    // Ask for confirmation before removing a book.
    document.querySelectorAll(".remove-form").forEach((form) => {
        form.addEventListener("submit", (event) => {
            const confirmed = window.confirm("Remove this book?");
            if (!confirmed) {
                event.preventDefault();
            }
        });
    });

    // Client-side checkout phone validation.
    const checkoutForm = document.getElementById("checkoutForm");
    const phoneInput = document.getElementById("phone");
    const phoneError = document.getElementById("phoneError");

    if (checkoutForm && phoneInput) {
        checkoutForm.addEventListener("submit", (event) => {
            const phone = phoneInput.value.trim();

            if (!/^\d{10}$/.test(phone)) {
                event.preventDefault();
                if (phoneError) {
                    phoneError.textContent = "Phone number must be exactly 10 digits.";
                }
                phoneInput.focus();
            } else if (phoneError) {
                phoneError.textContent = "";
            }
        });

        phoneInput.addEventListener("input", () => {
            phoneInput.value = phoneInput.value.replace(/\D/g, "").slice(0, 10);
            if (/^\d{10}$/.test(phoneInput.value) && phoneError) {
                phoneError.textContent = "";
            }
        });
    }

    // Hide green flash messages after 3 seconds.
    window.setTimeout(() => {
        document.querySelectorAll(".flash.success").forEach((message) => {
            message.classList.add("fade-out");
            window.setTimeout(() => message.remove(), 400);
        });
    }, 3000);

    // Simple mobile navbar.
    const menuToggle = document.getElementById("menuToggle");
    const navLinks = document.getElementById("navLinks");

    if (menuToggle && navLinks) {
        menuToggle.addEventListener("click", () => {
            navLinks.classList.toggle("open");
        });
    }
});
