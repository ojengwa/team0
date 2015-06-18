$(document).ready(function () {
  var user_id = localStorage.getItem('user_id');

  if (user_id != null) {
    $.ajax({
      type: "GET",
      url: "http://45.55.84.195/v1/files?owner=" + user_id,
      crossDomain: true,
      dataType: "json"
    })
    .done(function (data, statusText) {
      if (data.hasOwnProperty("files")) {
        displayHistory(data.files);
      }
    })
    .fail(function (xhr, statusText) {

    });
  }
});

var displayHistory = function (files) {
  var dates = sortFilesByDate(files);

  for (date in dates) {
    var dateTemplate = "<div class='row date'>" +
                          "<div class='col-md-12'>" +
                            "<h5>" + date + "</h5>" +
                          "</div>" +
                        "</div>";

    $("#history").append(dateTemplate);

    dates[date].forEach(function (file) {
      var fileTemplate = "<div class='row file'>" +
                            "<div class='col-md-8'>" +
                              "<a href='" + file["html_url"] + "'>" + file["html_url"] + "</a>" +
                            "</div>" +
                            "<div class='col-md-4'>" +
                              "<a id='openPDFButton' href='pdf/web/viewer.html?file=" + file.url + "' class='btn btn-default'>Open PDF</a>" +
                              "<a id='downloadPDFButton' href='" + file.url + "' class='btn btn-primary'>Download PDF</a>"
                            "</div>" +
                          "</div>";

      $("#history").append(fileTemplate);
    });
  }
};

var sortFilesByDate = function (files) {
  var dates = {};

  var l = files.length;
  for (var i = 0; i < l; ++i) {
    var file = files[i];
    var date = new Date(file["created_at"]).toDateString();

    if (!dates.hasOwnProperty(date)) {
      dates[date] = [];
    }

    dates[date].push(file);
  }

  return dates;
}