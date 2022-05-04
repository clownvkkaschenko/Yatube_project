const swt = document.querySelector(".switchMode", ".swm > span");
const theme = document.querySelector("#theme", "#theme1");
swt.addEventListener("click", function() {
  if (theme.getAttribute("href") == "/static/css/light.css") {
    theme.href = "/static/css/dark.css";
  } else {
    theme.href = "/static/css/light.css";
  }
  {swt.innerHTML =
    (swt.innerHTML === 'Light Mode') ? swt.innerHTML = 'Dark Mode' : swt.innerHTML = 'Light Mode';}
});