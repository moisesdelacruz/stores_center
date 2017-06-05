module.exports = function (review) {
  var el = ``
  for (var i = 0; i < 5; i++) {
    if (review <= i) {
      el+=`<i class="fa fa-star-o" aria-hidden="true" data-index="${i}"></i>`
    } else {
      el+=`<i class="fa fa-star" aria-hidden="true" data-index="${i}"></i>`
    }
  }
  return el
}
