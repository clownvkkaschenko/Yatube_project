const swt = document.getElementById('theme-toggle')
const img = document.getElementById('tt-img')

swt.addEventListener('click', function() {
  if (document.body.classList.contains('dark')) {
    document.body.classList.remove('dark')
    img.src='/static/img/mode/moon.png'
    localStorage.theme = 'light'
  } else {
    document.body.classList.add('dark')
    img.src='/static/img/mode/sun.png'
    localStorage.theme = 'dark'
  }
})

if (localStorage.theme =='dark') {
  document.body.classList.add('dark')
  img.src='/static/img/mode/sun.png'
}