// A callback to call when the Google API has finished loading.
function onGApiLoad() {
    gapi.auth2.getAuthInstance().currentUser.listen(function (googleUser) {

      var profile = googleUser.getBasicProfile();

      if (profile !== undefined) {
        localStorage.setItem('user_id', profile.getEmail());
      }
    });
}