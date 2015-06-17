function loading(filename) {
  var url = "http://mozilla.github.io/pdf.js/web/viewer.html";
  var add = "?file=".concat(encodeURIComponent(filename));
  var res = encodeURIComponent(add);
  var page = url.concat(add);

  window.location.href=page;
}

// Attach a submit handler to the form
$( "#submitpdf" ).click(function( event ) {
 
    // Stop form from submitting normally
    event.preventDefault();
     
    var data = {};
    data["url"] = $("#urltext").val();
    addData(data);
});

// send the data using post to the app's url
function addData(data){
    $.ajax({
        type: "POST",
        url: "http://aqueous-atoll-7901.herokuapp.com/v1/files",
        data: JSON.stringify(data),
        contentType: "application/json; charset=utf-8",
        crossDomain: true,
        dataType: "json",
        success: function (result, status) {
            processResponse(result);
        }
    });
}

function processResponse(data){
    loading(data.url);
}