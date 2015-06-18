$(document).ready(function () {
  $("#url").focus();

  $("#submit").click(function (event) {
    event.preventDefault();
      
    clear();

    var data = {
      url: $("#url").val()
    };

    if (!(data.url.startsWith('http://') || data.url.startsWith('https://'))) {
      data.url = "http://" + data.url;
    }

    if (user != null) {
      data["user_id"] = user.getBasicProfile().getEmail();
    }

    $.ajax({
      type: "POST",
      url: "http://45.55.84.195/v1/files",
      data: JSON.stringify(data),
      contentType: "application/json; charset=utf-8",
      crossDomain: true,
      dataType: "json",
    })
    .done(function (data, statusText) {
      if (data.hasOwnProperty("url")) {
        displayPDF(data.url);
      }
    })
    .fail(function (xhr, statusText) {
      var response = xhr.responseJSON;

      if (response.hasOwnProperty("errors")) {
        var errors = response.errors;
        var message = errors[0].message;

        $("#urlForm").addClass("has-error");
        $("#urlLabel").text(message);
      }
    });
  });

  $("#signOutButton").click(function () {
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function () {
      $("#signinForm").css("display", "block");
      $("#userActions").css("visibility", "hidden");

      $("#userEmail").text("");

      user = null;
    });
  });
});

var displayPDF = function (url) {
  window.location.href = "pdf/web/viewer.html?file=" + encodeURIComponent(url);
};

var onSignIn = function (user) {
  var profile = user.getBasicProfile();

  $("#signinForm").css("display", "none");
  $("#userActions").css("visibility", "visible");

  $("#userEmail").text(profile.getEmail());
};

var clear = function () {
  $("#urlForm").attr("class", "form-group");
  $("#urlLabel").text("");
};