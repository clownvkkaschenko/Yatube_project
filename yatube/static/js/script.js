if (!localStorage.theme) localStorage.theme = "light"
document.body.className = localStorage.theme

const swt = document.querySelector("#theme-toggle", ".swt > span");

swt.addEventListener("click", function() {
  document.body.classList.toggle("dark")
  localStorage.theme = document.body.className || "light"
});