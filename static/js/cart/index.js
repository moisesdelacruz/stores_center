const getCookie = require('../get_cookie.js');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function addEventListenerByClass(className, event, fn) {
  var list = document.getElementsByClassName(className);
  for (var i = 0, len = list.length; i < len; i++) {
    list[i].addEventListener(event, fn, false);
  }
}

// add to cart
addEventListenerByClass('add_or_remove_product_cart', 'click', eventAddOrRemove);

function eventAddOrRemove(event) {
  event.preventDefault();
  action = this.getAttribute('data-action');

  if (action == 'add') {
    addToCart(event);
  } else {
    removeFromCart(event);
  }
}

function addToCart(event) {

  var el = event.target.closest('.product')
    ? event.target.closest('.product')
    : event.target.closest('.product_detail');

  var quantity_element = el.getElementsByClassName('quantity')[0];
  var quantity = 1;
  if (quantity_element) {
    quantity = quantity_element.value;
    if (quantity_element.value > quantity_element.max) {
      quantity = quantity_element.max;
    }
  }

  var product = {
    'product': el.getAttribute('data-id'),
    'quantity': quantity
  };

  var csrftoken = getCookie('csrftoken');

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
    context: event.currentTarget,
    success: function (response) {
      if (response.created) {
        let count_product_cart = document.getElementById('cart_count');
        count_product_cart.textContent = parseInt(count_product_cart.textContent)+1;
        this.classList.remove('orange');
        this.classList.add('red');
        this.querySelector('i').innerText = "remove_shopping_cart";
        this.setAttribute('data-action', 'remove');
        if (this.querySelector('span')) {
          this.querySelector('span').innerText = "REMOVE FROM CART";
        }
      } else {
        alert('product already exist in your collection');
      }
    }
  });
}


// remove from cart
function removeFromCart(event) {

  var el = event.target.closest('.product')
    ? event.target.closest('.product')
    : event.target.closest('.product_detail');

  var product = {
    'product': el.getAttribute('data-id')
  };

  var csrftoken = getCookie('csrftoken');

  $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
      }
  });

  $.ajax({
    type: 'POST',
    url: '/shopping_cart/remove/',
    data: product,
    context: event.currentTarget,
    success: function (response) {
      if (response.success) {
        let count_product_cart = document.getElementById('cart_count');
        count_product_cart.textContent = parseInt(count_product_cart.textContent)-1;
        if (window.location.pathname === "/shopping_cart/") {
          this.closest('.product').parentElement.removeChild(this.closest('.product'));
          return;
        }
        this.classList.remove('red');
        this.classList.add('orange');
        this.querySelector('i').innerText = "add_shopping_cart";
        this.setAttribute('data-action', 'add');
        if (this.querySelector('span')) {
          this.querySelector('span').innerText = "ADD TO CART";
        }
      } else {
        alert('product not exist in your collection');
      }
    }
  });
}
