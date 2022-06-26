const swt = document.getElementById('theme-toggle')
const img = document.getElementById('tt-img')
const menu = document.getElementById('menu-icon')

swt.addEventListener('click', function() {
  if (document.body.classList.contains('dark')) {
    document.body.classList.remove('dark')
    img.src='/static/img/mode/moon.png'
    menu.src='/static/img/mode/menu5.png'
    localStorage.theme = 'light'
  } else {
    document.body.classList.add('dark')
    img.src='/static/img/mode/sun.png'
    menu.src='/static/img/mode/dark-menu5.png'
    localStorage.theme = 'dark'
  }
})

if (localStorage.theme =='dark') {
  document.body.classList.add('dark')
  img.src='/static/img/mode/sun.png'
  menu.src='/static/img/mode/dark-menu5.png'
}