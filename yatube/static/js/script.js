const swt = document.querySelector("#theme-toggle", ".swt > span");
const theme = document.querySelector("#test_theme");
swt.addEventListener("click", function() {
  if (theme.getAttribute("href") == "/static/css/style.css") {
    theme.href = "/static/css/dark.css";
  } else {
    theme.href = "/static/css/style.css";
  }
});