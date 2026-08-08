const pages = [
    document.getElementById("welcome"),
    document.getElementById("language")
];

const backButton = document.getElementById("back");
const nextButton = document.getElementById("next");
const statusText = document.getElementById("status");

const languageSelect = document.getElementById("language-select");

let currentPage = 0;

const installConfig = {
    language: "en"
};

function showPage(page) {
    pages.forEach((element, index) => {
        element.classList.toggle(
            "hidden",
            index !== page
        );
    });

    backButton.disabled = page === 0;

    nextButton.textContent =
        page === pages.length - 1
            ? "Next >"
            : "Next >";

    statusText.textContent =
        `Step ${page + 1} of ${pages.length}`;
}


function next() {
    if (currentPage === 1) {
        installConfig.language =
            languageSelect.value;
    }

    if (currentPage < pages.length - 1) {
        currentPage++;
        showPage(currentPage);
    }
}

function back() {
    if (currentPage > 0) {
        currentPage--;
        showPage(currentPage);
    }
}

nextButton.addEventListener("click", next);
backButton.addEventListener("click", back);
showPage(currentPage);