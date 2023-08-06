window.userplus = {
  fbLoginInit: function(appId, buttonSelector, formSelector, errorCb) {
    window.fbAsyncInit = function() {
      FB.init({
        appId: appId,
        xfbml: true,
        version: 'v2.6'
      });
    };

    (function(d, s, id) {
      var js, fjs = d.getElementsByTagName(s)[0];
      if (d.getElementById(id)) {
        return;
      }
      js = d.createElement(s);
      js.id = id;
      js.src = "//connect.facebook.net/en_US/sdk.js";
      fjs.parentNode.insertBefore(js, fjs);
    }(document, 'script', 'facebook-jssdk'));

    document.querySelector(buttonSelector).addEventListener('click', function(e) {
      e.preventDefault();
      FB.login(function(res) {
        if (res.status === 'connected' && FB.api('me').email) {
          var form = document.querySelector(formSelector);
          form.querySelector('input[name=access_token]').value = res.authResponse.accessToken;
          form.submit()
        } else if (errorCb) {
          errorCb();
        }
      }, { scope: 'public_profile,email' });
    })
  }
}
