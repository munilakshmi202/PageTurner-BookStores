document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("bookSearch");
    const bookGrid = document.getElementById("bookGrid");
    const noSearch = document.getElementById("noSearch");

    if (searchInput && bookGrid) {
        const bookCards = Array.from(
            bookGrid.querySelectorAll(".book-card")
        );

        function filterBooks() {
            const searchText = searchInput.value.trim().toLowerCase();
            let visibleBooks = 0;

            bookCards.forEach(function (card) {
                const title = card.dataset.title || "";
                const author = card.dataset.author || "";

                if (
                    title.includes(searchText) ||
                    author.includes(searchText)
                ) {
                    card.style.display = "";
                    visibleBooks++;
                } else {
                    card.style.display = "none";
                }
            });

            if (noSearch) {
                noSearch.hidden = visibleBooks !== 0;
            }
        }

        searchInput.addEventListener("input", filterBooks);
    }

    const flashMessages = document.querySelectorAll(".flash");

    flashMessages.forEach(function (message) {
        setTimeout(function () {
            message.style.opacity = "0";
            message.style.transform = "translateY(-10px)";
            message.style.transition = "all 0.4s ease";

            setTimeout(function () {
                message.remove();
            }, 400);
        }, 4000);
    });
});
