const themeToggle = document.getElementById("theme-toggle");

function updateThemeButton() {
  if (document.body.classList.contains("dark-mode")) {
    themeToggle.textContent = "☀️";
    themeToggle.setAttribute("aria-label", "Switch to light mode");
    themeToggle.setAttribute("title", "Switch to light mode");
  } else {
    themeToggle.textContent = "🌙";
    themeToggle.setAttribute("aria-label", "Switch to dark mode");
    themeToggle.setAttribute("title", "Switch to dark mode");
  }
}

if (localStorage.getItem("cloudforge-theme") === "dark") {
  document.body.classList.add("dark-mode");
}

updateThemeButton();

themeToggle.addEventListener("click", () => {
  document.body.classList.toggle("dark-mode");

  const theme = document.body.classList.contains("dark-mode")
    ? "dark"
    : "light";

  localStorage.setItem("cloudforge-theme", theme);
  updateThemeButton();
});
