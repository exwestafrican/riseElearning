
var items = document.querySelectorAll('.item')



document.querySelector(".myToggler").addEventListener('click',function() {
  for (let i = 0; i < items.length; i++) {
    items[i].classList.toggle('active')
    
  }

})