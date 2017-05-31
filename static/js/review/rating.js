function addEventListenerByClass(className, event, fn) {
  var list = document.getElementsByClassName(className);
  for (var i = 0, len = list.length; i < len; i++) {
    list[i].addEventListener(event, fn, false);
  }
}

addEventListenerByClass('rating', 'click', fun_rating);

function fun_rating(event) {
  var el = event.target

  var star = el.getAttribute('data-index');
  for (var i = 0; i < star; i++) {
  	this.children[i].classList.add('active');
  }

  for (var i = star; i < 5; i++) {
    this.children[i].classList.remove('active');
  }
  debugger
  var product = {
    "id": el.parentElement.getAttribute('data-product'),
    "name": el.parentElement.parentElement.parentElement.querySelectorAll('.title')[0].innerText,
    "rating": star
  }

  var form = `<form id="review_comment"
    method="post" class="content_comment">
    <h4 class="title">${product.name}</h4>
      <textarea id="comment"></textarea>
    <button class="btn right" type="submit">
      <i class="material-icons right">send</i>
      Submit
    </button>
  </form>`

  // const content = document.getElementById('review_content');
  var floting = document.createElement('div');
  floting.setAttribute('id', 'review_content');
  floting.innerHTML = form;
  if (document.body.appendChild(floting)) {
    var module_form = require('./review.js');
    module_form(product);
  }
}
