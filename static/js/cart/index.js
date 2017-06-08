const getCookie = require('../get_cookie.js');

function addEventListenerByClass(className, event, fn) {
  var list = document.getElementsByClassName(className);
  for (var i = 0, len = list.length; i < len; i++) {
    list[i].addEventListener(event, fn, false);
  }
}

// add to cart
addEventListenerByClass('add_to_cart', 'click', addToCart);

function addToCart(event) {
  event.preventDefault();
  var el = event.target.closest('.product')
    ? event.target.closest('.product')
    : event.target.closest('.product_detail');

  var product = {
    'product': el.getAttribute('data-id')
  };

  var csrftoken = getCookie('csrftoken');

  function csrfSafeMethod(method) {
      // these HTTP methods do not require CSRF protection
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
      }
  });

  $.ajax({
    type: 'POST',
    url: '/shopping_cart/add/',
    data: product,
    success: function (response) {
      if (response.created) {
        let count_product_cart = document.getElementById('cart_count');
        count_product_cart.textContent = parseInt(count_product_cart.textContent)+1;
      } else {
        alert('product already exist in your collection');
      }
    }
  });
}
