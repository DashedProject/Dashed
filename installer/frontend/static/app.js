const API_URL = `http://${window.location.hostname}:7001`;

const pages = [
    document.getElementById("welcome"),
    document.getElementById("language"),
    document.getElementById("region"),
    document.getElementById("keyboard"),
    document.getElementById("hostname"),
    document.getElementById("account"),
    document.getElementById("disk"),
    document.getElementById("summary")
];

const backButton = document.getElementById("back");
const nextButton = document.getElementById("next");
const statusText = document.getElementById("status");

const languageSelect = document.getElementById("language-select");
const regionSelect = document.getElementById("region-select");
const keyboardSelect = document.getElementById("keyboard-select");

const hostnameInput = document.getElementById("hostname-input");
const hostnameError = document.getElementById("hostname-error");

const usernameInput = document.getElementById("username");
const passwordInput = document.getElementById("password");
const passwordConfirmInput = document.getElementById("password-confirm");

const accountError = document.getElementById("account-error");
const diskList = document.getElementById("disk-list");
const diskError = document.getElementById("disk-error");

const summaryLanguage = document.getElementById("summary-language");
const summaryRegion = document.getElementById("summary-region");
const summaryKeyboard = document.getElementById("summary-keyboard");
const summaryHostname = document.getElementById("summary-hostname");
const summaryUsername = document.getElementById("summary-username");
const summaryDisk = document.getElementById("summary-disk");

let currentPage = 0;

const installConfig = {
    language: "en",
    region: "US",
    keyboard: "us",
    hostname: "",
    username: "",
    password: "",
    disk: null
};

function updateSummary() {
    summaryLanguage.textContent = installConfig.language;
    summaryRegion.textContent = installConfig.region;
    summaryKeyboard.textContent = installConfig.keyboard;
    summaryHostname.textContent = installConfig.hostname;
    summaryUsername.textContent = installConfig.username;
    summaryDisk.textContent = installConfig.disk || "None";
}

function showPage(page) {
    pages.forEach((element, index) => {
        element.classList.toggle("hidden", index !== page);
    });

    backButton.disabled = page === 0;

    if (page === pages.length - 1) {
        nextButton.textContent = "Install";
    } else {
        nextButton.textContent = "Next >";
    }

    statusText.textContent =
        `Step ${page + 1} of ${pages.length}`;

    if (page === 6) {
        loadDisks();
    }

    if (page === 7) {
        updateSummary();
    }
}

function saveCurrentPage() {
    if (currentPage === 1) {
        installConfig.language = languageSelect.value;
    }

    if (currentPage === 2) {
        installConfig.region = regionSelect.value;
    }

    if (currentPage === 3) {
        installConfig.keyboard = keyboardSelect.value;
    }

    if (currentPage === 4) {
        installConfig.hostname =
            hostnameInput.value.trim();
    }

    if (currentPage === 5) {
        installConfig.username =
            usernameInput.value.trim();

        installConfig.password =
            passwordInput.value;
    }

    if (currentPage === 6) {
        const selectedDisk = document.querySelector(
            'input[name="disk"]:checked'
        );

        if (selectedDisk) {
            installConfig.disk =
                selectedDisk.value;
        }
    }
}

function validateHostname() {
    const hostname =
        hostnameInput.value.trim();

    if (hostname.length === 0) {
        hostnameError.textContent =
            "Please enter a hostname.";

        hostnameError.classList.remove("hidden");

        return false;
    }

    if (hostname.length > 63) {
        hostnameError.textContent =
            "Hostname cannot be longer than 63 characters.";

        hostnameError.classList.remove("hidden");

        return false;
    }

    if (!/^[a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]$/.test(hostname)) {
        hostnameError.textContent =
            "Hostname may only contain letters, numbers, and hyphens.";

        hostnameError.classList.remove("hidden");

        return false;
    }

    hostnameError.classList.add("hidden");

    return true;
}

function validateCurrentPage() {
    if (currentPage === 4) {
        return validateHostname();
    }

    if (currentPage !== 5) {
        return true;
    }

    const username =
        usernameInput.value.trim();

    const password =
        passwordInput.value;

    const confirmation =
        passwordConfirmInput.value;

    if (username.length === 0) {
        accountError.textContent =
            "Please enter a username.";

        accountError.classList.remove("hidden");

        return false;
    }

    if (username.includes(" ")) {
        accountError.textContent =
            "Username cannot contain spaces.";

        accountError.classList.remove("hidden");

        return false;
    }

    if (password.length === 0) {
        accountError.textContent =
            "Please enter a password.";

        accountError.classList.remove("hidden");

        return false;
    }

    if (password !== confirmation) {
        accountError.textContent =
            "The passwords do not match.";

        accountError.classList.remove("hidden");

        return false;
    }

    accountError.classList.add("hidden");

    return true;
}

async function loadDisks() {
    diskList.innerHTML =
        "<p>Loading disks...</p>";

    diskError.classList.add("hidden");

    try {
        const response = await fetch(
            `${API_URL}/disks`
        );

        if (!response.ok) {
            throw new Error("Failed to load disks.");
        }

        const disks = await response.json();

        diskList.innerHTML = "";

        if (disks.length === 0) {
            diskList.innerHTML =
                "<p>No disks were found.</p>";

            installConfig.disk = null;

            return;
        }

        disks.forEach((disk, index) => {
            const label =
                document.createElement("label");

            label.className =
                "disk-option";

            const radio =
                document.createElement("input");

            radio.type = "radio";
            radio.name = "disk";
            radio.value = disk.device;
            radio.checked = index === 0;

            radio.addEventListener("change", () => {
                installConfig.disk =
                    disk.device;

                diskError.classList.add("hidden");
            });

            const text =
                document.createElement("span");

            text.textContent =
                `${disk.device} — ${disk.size} — ${disk.model}`;

            label.appendChild(radio);
            label.appendChild(text);

            diskList.appendChild(label);
        });

        installConfig.disk =
            disks[0].device;

    } catch (error) {
        diskList.innerHTML = "";

        diskError.textContent =
            "Could not connect to the Dashed setup API.";

        diskError.classList.remove("hidden");

        installConfig.disk = null;
    }
}

async function startInstallation() {
    if (!installConfig.disk) {
        alert("Please select an installation disk.");
        return;
    }

    const confirmed = confirm(
        `WARNING!\n\n` +
        `Installing Dashed will erase ${installConfig.disk}.\n\n` +
        `Are you sure you want to continue?`
    );

    if (!confirmed) {
        return;
    }

    nextButton.disabled = true;
    backButton.disabled = true;

    statusText.textContent =
        "Installing Dashed...";

    try {
        const response = await fetch(
            `${API_URL}/install`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(installConfig)
            }
        );

        const result =
            await response.json();

        if (!response.ok) {
            throw new Error(
                result.detail ||
                "Installation failed."
            );
        }

        statusText.textContent =
            "Installation complete.";

        console.log(result);

    } catch (error) {
        statusText.textContent =
            "Installation failed.";

        alert(error.message);

        nextButton.disabled = false;
        backButton.disabled = false;
    }
}

function next() {
    if (!validateCurrentPage()) {
        return;
    }

    saveCurrentPage();

    if (currentPage === 6) {
        const selectedDisk =
            document.querySelector(
                'input[name="disk"]:checked'
            );

        if (!selectedDisk) {
            diskError.textContent =
                "Please select a disk.";

            diskError.classList.remove("hidden");

            return;
        }

        installConfig.disk =
            selectedDisk.value;
    }

    if (currentPage < pages.length - 1) {
        currentPage++;
        showPage(currentPage);
    } else {
        startInstallation();
    }
}

function back() {
    if (currentPage > 0) {
        currentPage--;
        showPage(currentPage);
    }
}

nextButton.addEventListener(
    "click",
    next
);

backButton.addEventListener(
    "click",
    back
);

showPage(currentPage);