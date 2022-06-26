document.querySelector('.btn_comment').addEventListener('click', function (e) {
    var div = document.querySelector('div.form_comments')
    div.style.display = div.style.display === 'none' ? 'block' : 'none'
  })