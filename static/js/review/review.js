function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

module.exports = function(review) {
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
    }

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
}
