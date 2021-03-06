(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
const getCookie = require('../get_cookie.js');

function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method)
  );
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

  var el = event.target.closest('.product') ? event.target.closest('.product') : event.target.closest('.product_detail');

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
    beforeSend: function (xhr, settings) {
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
        count_product_cart.textContent = parseInt(count_product_cart.textContent) + 1;
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

  var el = event.target.closest('.product') ? event.target.closest('.product') : event.target.closest('.product_detail');

  var product = {
    'product': el.getAttribute('data-id')
  };

  var csrftoken = getCookie('csrftoken');

  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
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
        count_product_cart.textContent = parseInt(count_product_cart.textContent) - 1;
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

},{"../get_cookie.js":2}],2:[function(require,module,exports){
module.exports = function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === name + '=') {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

},{}],3:[function(require,module,exports){
$(document).ready(function () {
   $('select').material_select();

   require('./review/rating.js');
   require('./cart/index.js');
   require('./pay/index.js');
});

},{"./cart/index.js":1,"./pay/index.js":4,"./review/rating.js":5}],4:[function(require,module,exports){
const getCookie = require('../get_cookie.js');
const btn_shop_all = document.getElementById('shop_all');

function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method)
  );
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
  };
  payNow(product);
}

// method pay product
function payProducts(event) {
  event.preventDefault();

  var el = event.target.closest('.product') ? event.target.closest('.product') : event.target.closest('.product_detail');

  var product = {
    'product': el.getAttribute('data-id')
  };

  payNow(product);
}

function payNow(product) {
  var csrftoken = getCookie('csrftoken');

  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
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
                  count_product_cart.textContent = parseInt(count_product_cart.textContent) - 1;
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

},{"../get_cookie.js":2}],5:[function(require,module,exports){
function addEventListenerByClass(className, event, fn) {
  var list = document.getElementsByClassName(className);
  for (var i = 0, len = list.length; i < len; i++) {
    list[i].addEventListener(event, fn, false);
  }
}

addEventListenerByClass('rating', 'click', fun_rating);

function fun_rating(event) {
  var el = event.target;

  var star = el.getAttribute('data-index');
  for (var i = 0; i < star; i++) {
    this.children[i].classList.add('active');
  }

  for (var i = star; i < 5; i++) {
    this.children[i].classList.remove('active');
  }
  debugger;
  var product = {
    "id": el.parentElement.getAttribute('data-product'),
    "name": el.parentElement.parentElement.parentElement.querySelectorAll('.title')[0].innerText,
    "rating": star
  };

  var form = `<form id="review_comment"
    method="post" class="content_comment">
    <h4 class="title">${product.name}</h4>
      <textarea id="comment"></textarea>
    <button class="btn right" type="submit">
      <i class="material-icons right">send</i>
      Submit
    </button>
  </form>`;

  // const content = document.getElementById('review_content');
  var floting = document.createElement('div');
  floting.setAttribute('id', 'review_content');
  floting.innerHTML = form;
  if (document.body.appendChild(floting)) {
    var module_form = require('./review.js');
    module_form(product);
  }
}

},{"./review.js":6}],6:[function(require,module,exports){
const getCookie = require('../get_cookie.js');

module.exports = function (review) {
  const review_comment = document.getElementById('review_comment');
  if (review_comment) {
    review_comment.addEventListener('submit', send_review);
  }

  function send_review(event) {
    event.preventDefault();
    var el = event.target;

    var csrftoken = getCookie('csrftoken');

    var data = {
      "product": review,
      "comment": el.querySelectorAll('#comment')[0].value
    };

    function csrfSafeMethod(method) {
      // these HTTP methods do not require CSRF protection
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method)
      );
    }
    $.ajaxSetup({
      beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      }
    });

    $.ajax({
      type: 'POST',
      url: '/review/',
      data: data,
      success: function (response) {
        const review_content = document.getElementById('review_content');
        review_content.parentNode.removeChild(review_content);
        if (document.getElementById('reviews')) {
          comment_review(response);
        }
      }
    });

    function comment_review(data) {
      review = JSON.parse(data.object);
      stars = require('./star.js');
      debugger;

      el = `<div class="card-stacked">
          <div class="card-content">
              <a
                href="@${review.user}"
                class="username">@${review.user}</a>
            <p>${review.comment}</p>
          </div>
          <div class="card-action">
            <span class="left" data-product="${review.product.id}">
              ${stars(review.rating)}
            </span>
          </div>
        </div>`;

      var card = document.createElement('div');
      card.setAttribute('class', 'card horizontal card_comment');
      card.innerHTML = el;
      // append to
      var reviews_content = document.getElementById('reviews');
      if (data.created) {
        reviews_content.prepend(card);
      } else {
        for (var i = 0; i < reviews_content.children.length; i++) {
          let actual = reviews_content.children[i];
          if (actual.getAttribute('data-user') === review.user) {
            reviews_content.replaceChild(card, actual);
            return;
          }
        }
      }
    }
  }
};

},{"../get_cookie.js":2,"./star.js":7}],7:[function(require,module,exports){
module.exports = function (review) {
  var el = ``;
  for (var i = 0; i < 5; i++) {
    if (review <= i) {
      el += `<i class="fa fa-star-o" aria-hidden="true" data-index="${i}"></i>`;
    } else {
      el += `<i class="fa fa-star" aria-hidden="true" data-index="${i}"></i>`;
    }
  }
  return el;
};

},{}]},{},[3]);
