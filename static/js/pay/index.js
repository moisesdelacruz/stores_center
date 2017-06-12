const getCookie = require('../get_cookie.js');
const btn_shop_all = document.getElementById('shop_all');

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

// Event pay all products
if (btn_shop_all) {
  btn_shop_all.addEventListener('click', payAllProducts, false);
}

// Event pay one product
addEventListenerByClass('shop_now', 'click', payProducts);

// method pay all products
function payAllProducts(event) {
  event.preventDefault();
  var product = {
    'product': 'all'
  }
  payNow(product)
}

// method pay product
function payProducts(event) {
  event.preventDefault();

  var el = event.target.closest('.product')
    ? event.target.closest('.product')
    : event.target.closest('.product_detail');

  var product = {
    'product': el.getAttribute('data-id')
  };

  payNow(product)
}

function payNow(product) {
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
    url: '/shopping_cart/pay/',
    data: product,
    context: event.currentTarget,
    success: function (response, textStatus, xhr) {
      if (xhr.status === 200) {
        document.getElementById('user_money').textContent = response.user_money;

        let count_product_cart = document.getElementById('cart_count');

        if (window.location.pathname === "/shopping_cart/") {
          var list = document.getElementsByClassName('product');
          
          for (var i = 0, len = list.length; i < len; i++) {
            for (var x = 0; x < response.sold.length; x++) {
              if (list[i]) {
                if (response.sold[x] === list[i].getAttribute('data-id')) {
                  count_product_cart.textContent = parseInt(count_product_cart.textContent)-1;
                  list[i].parentElement.removeChild(list[i]);
                }
              }
            }
          }
        }
      } else {
        console.log(`no tienes suficiente dinero :/ - total:\$ ${response.total_pay}`);
        return;
      }
    }
  });
}
