function loading(filename) {
  var url = "http://mozilla.github.io/pdf.js/web/viewer.html";
  var add = "?file=".concat(encodeURIComponent(filename));
  var res = encodeURIComponent(add);
  var page = url.concat(add);

  window.location.href=page;
}