document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector(".admin-form");

    form.addEventListener("submit", (e) => {
        const inputs = form.querySelectorAll("input, textarea");
        for (let field of inputs) {
            if (!field.value.trim()) {
                alert("Please fill all fields");
                e.preventDefault();
                return;
            }
        }
    });
});
