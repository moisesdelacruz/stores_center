(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
$(document).ready(function () {
   $('select').material_select();

   require('./review/rating.js');
});

},{"./review/rating.js":2}],2:[function(require,module,exports){
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

},{"./review.js":3}],3:[function(require,module,exports){
function getCookie(name) {
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
}

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
            }
        });

        // var xhr = new XMLHttpRequest();
        // xhr.open('POST', '/review/', true);
        // xhr.setRequestHeader('X-CSRFToken', csrftoken);
        // xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
        // xhr.onload = function() {
        //     if (xhr.status === 202) {
        //         console.log(xhr.responseText);
        //     }
        // };
        // xhr.send(JSON.stringify(data));
    }
};

},{}]},{},[1]);
