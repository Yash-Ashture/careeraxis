function togglePassword() {
    const pwd = document.getElementById("password");
    pwd.type = pwd.type === "password" ? "text" : "password";
}

document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    const btn = document.querySelector(".login-btn");

    if (form) {
        form.addEventListener("submit", () => {
            btn.classList.add("loading");
        });
    }
});
document.addEventListener("DOMContentLoaded", () => {
    const card = document.querySelector(".profile-card");
    if (card) {
        card.style.opacity = "1";
    }
});

