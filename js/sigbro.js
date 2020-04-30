// PRODUCTION
var APIURL = "https://sigbro-wallet.api.nxter.org"
var TEMPLATEURL = "https://sigbro-template.api.nxter.org"

// DEVELOPMENT
// var TEMPLATEURL = "http://localhost:9060"
// var APIURL = "http://localhost:8020"

var TIMEOUT_TEMPLATE = 10000;
var TIMEOUT_SUBMIT = 10000;
var TIMEOUT_ARDR = 3000;

$(document).on('click', 'a.nav-link', function (e) {
  e.preventDefault();
  var open_page = $(this).attr('href').replace('#', '');

  if (open_page == 'profile') {
    localStorage.setItem("sigbro_wallet_page", "profile");
    show_profile();
    return;
  }

  if (open_page == 'balances') {
    localStorage.setItem("sigbro_wallet_page", "balances");
    show_balances();
    return;
  }

  if (open_page == 'operations') {
    localStorage.setItem("sigbro_wallet_page", "operations");
    show_operations();
    return;
  }

  if (open_page == 'alerts') {
    localStorage.setItem("sigbro_wallet_page", "alerts");
    show_alerts();
    return;
  }

  if (open_page == 'offline') {
    localStorage.setItem("sigbro_wallet_page", "offline");
    show_offline_page();
    return;
  }

});

$(document).ready(function () {
  var page = localStorage.getItem("sigbro_wallet_page");
  //console.log("Last page: " + page);
  if (page == null) { page = 'index'; }

  if (page == 'index') { show_index(); return; }
  if (page == 'balances') { show_balances(); return; }
  if (page == 'profile') { show_profile(); return; }
  if (page == 'operations') { show_operations(); return; }
  if (page == 'alerts') { show_alerts(); return; }
  if (page == 'offline') { show_offline_page(); return; }

});

// alerts for the offline page
function page_offline_hide_alert() {
  var msg_block = document.getElementById('sigbro_offline--alerts');
  msg_block.setAttribute('style', 'display:none;');
}

function page_offline_show_alert(msg) {
  var msg_block = document.getElementById('sigbro_offline--alerts');
  msg_block.setAttribute('style', 'display:none;');

  document.getElementById('sigbro_offline--alerts_text').innerHTML = msg;
  msg_block.setAttribute('style', '');
}

// alerts for the alerts page
function page_alerts_hide_alert() {
  var msg_block = document.getElementById('sigbro_alerts--alerts');
  msg_block.setAttribute('style', 'display:none;');
}

function page_alerts_show_alert(msg) {
  var msg_block = document.getElementById('sigbro_alerts--alerts');
  msg_block.innerHTML = msg;
  msg_block.setAttribute('style', '');
}

function check_session() {
  var resp = this.responseText;

  if (resp) {
    var resp_j = JSON.parse(resp);

    //console.log(resp_j);

    if (resp_j.result && resp_j.result == "fail") {
      // clear email and reload page
      localStorage.removeItem("sigbro_alerts_email");
      localStorage.removeItem("sigbro_alerts_token")

      page_alerts_show_alert(resp_j.msg);
      setTimeout(function () {
        show_alerts();
      }, 2000);
      return false;
    }

    return true;
  }

  var sigbro_alerts_token = localStorage.getItem("sigbro_alerts_token");
  var sigbro_alerts_email = localStorage.getItem("sigbro_alerts_email")

  payload = JSON.stringify(
    {
      "email": sigbro_alerts_email,
      "session": sigbro_alerts_token
    }
  );

  url = APIURL + "/api/v2/wallet/session/";

  sendJSON(url, payload, TIMEOUT_SUBMIT, check_session);

}

function page_alerts_get_accounts() {
  var resp = this.responseText;

  if (resp) {
    var resp_j = JSON.parse(resp);

    //console.log(resp_j);

    if (resp_j.result && resp_j.result == "ok") {
      if (resp_j.data) {
        localStorage.setItem("sigbro_alerts_cache_active_accounts", resp_j.data);
        document.getElementById('sigbro_alerts--account_list').innerHTML = resp_j.data;
      }

    } else {
      page_alerts_show_alert(resp_j.msg);
      setTimeout(function () {
        show_alerts();
      }, 2000);
      return false;
    }

    return true;
  }

  var page_cache = localStorage.getItem("sigbro_alerts_cache_active_accounts");
  if (page_cache != null) {
    document.getElementById('sigbro_alerts--account_list').innerHTML = page_cache;
  }

  var sigbro_alerts_token = localStorage.getItem("sigbro_alerts_token");
  var sigbro_alerts_email = localStorage.getItem("sigbro_alerts_email");

  payload = JSON.stringify(
    {
      "email": sigbro_alerts_email,
      "session": sigbro_alerts_token
    }
  );

  url = APIURL + "/api/v2/wallet/get-active-accounts/";

  sendJSON(url, payload, TIMEOUT_SUBMIT, page_alerts_get_accounts);

}

function page_alerts_get_inactive_accounts() {
  var resp = this.responseText;

  if (resp) {
    var resp_j = JSON.parse(resp);

    //console.log(resp_j);

    if (resp_j.result && resp_j.result == "ok") {
      if (resp_j.data) {
        localStorage.setItem("sigbro_alerts_cache_inactive_accounts", resp_j.data);
        document.getElementById('sigbro_alerts--inactive_account_list').innerHTML = resp_j.data;
      }

    } else {
      page_alerts_show_alert(resp_j.msg);
      setTimeout(function () {
        show_alerts();
      }, 2000);
      return false;
    }

    return true;
  }

  var page_cache = localStorage.getItem("sigbro_alerts_cache_inactive_accounts");
  if (page_cache != null) {
    document.getElementById('sigbro_alerts--inactive_account_list').innerHTML = page_cache;
  }

  var sigbro_alerts_token = localStorage.getItem("sigbro_alerts_token");
  var sigbro_alerts_email = localStorage.getItem("sigbro_alerts_email")

  payload = JSON.stringify(
    {
      "email": sigbro_alerts_email,
      "session": sigbro_alerts_token
    }
  );

  url = APIURL + "/api/v2/wallet/get-inactive-accounts/";

  sendJSON(url, payload, TIMEOUT_SUBMIT, page_alerts_get_inactive_accounts);

}

function show_alerts() {
  var sigbro_alerts_token = localStorage.getItem("sigbro_alerts_token");
  var sigbro_alerts_email = localStorage.getItem("sigbro_alerts_email");

  if (sigbro_alerts_token && sigbro_alerts_email) {
    //TODO: Check session and email


    $.ajax({
      url: 'alerts.html?_' + new Date().getTime(),
      type: 'GET',
      dataType: 'text',

      success: function (response) {
        $('#sigbro_spa').html(response);
        check_session();
        page_show_network_type();
        page_alerts_update_header();
        page_alerts_get_accounts();
        page_alerts_get_inactive_accounts();
      },

      error: function (error) {
        //console.log('ERROR: ', error);
      },

      complete: function (xhr, status) {
        //console.log('DONE');

        $(document).on('click', '#sigbro_alerts--add_acount', function (e) {
          e.preventDefault();
          document.getElementById("sigbro_alerts--add_acount").disabled = true;
          var sigbro_alerts_token = localStorage.getItem("sigbro_alerts_token");
          var sigbro_alerts_email = localStorage.getItem("sigbro_alerts_email");
          var sigbro_alerts_account = document.getElementById("sigbro_alerts--account_name").value;

          if (sigbro_alerts_account.length != 26) {
            page_alerts_show_alert("Wrong account format.");
            setTimeout(function () {
              document.getElementById("sigbro_alerts--add_acount").disabled = false;
            }, 2000);
            return false;
          }

          url = APIURL + "/api/v2/wallet/add_account/";
          payload = JSON.stringify({
            "email": sigbro_alerts_email,
            "session": sigbro_alerts_token,
            "accountRS": sigbro_alerts_account
          });

          sendJSON(url, payload, TIMEOUT_SUBMIT, page_alerts_add_account);
        });

        // change tx status
        $(document).on('click', '.sigbro-alerts-checkbox-transaction', function(e) {
          this.disabled = true;
          var button = this;

          var sigbro_alerts_token = localStorage.getItem("sigbro_alerts_token");
          var sigbro_alerts_email = localStorage.getItem("sigbro_alerts_email");
          var account_name = this.id.replace("sigbro_alerts--transaction_", "");

          var active = document.getElementById("sigbro_alerts--active_" + account_name).checked;
          var tx = document.getElementById("sigbro_alerts--transaction_" + account_name).checked;
          var block = document.getElementById("sigbro_alerts--block_" + account_name).checked;
          var approvals = document.getElementById("sigbro_alerts--approvals_" + account_name).checked;

          url = APIURL + "/api/v2/wallet/update_account/";
          payload = JSON.stringify({
            "email": sigbro_alerts_email,
            "session": sigbro_alerts_token,
            "accountRS": account_name,
            "active": active,
            "alert_tx": tx,
            "alert_block": block,
            "alert_approvals" : approvals,
          });

          sendJSON(url, payload, TIMEOUT_SUBMIT, page_alerts_update_account);

          setTimeout(function () {
            button.disabled = false;
          }, 2000);

        });

        // change forging status
        $(document).on('click', '.sigbro-alerts-checkbox-forging', function(e) {
          this.disabled = true;
          var button = this;

          var sigbro_alerts_token = localStorage.getItem("sigbro_alerts_token");
          var sigbro_alerts_email = localStorage.getItem("sigbro_alerts_email");
          var account_name = this.id.replace("sigbro_alerts--block_", "");

          var active = document.getElementById("sigbro_alerts--active_" + account_name).checked;
          var tx = document.getElementById("sigbro_alerts--transaction_" + account_name).checked;
          var block = document.getElementById("sigbro_alerts--block_" + account_name).checked;
          var approvals = document.getElementById("sigbro_alerts--approvals_" + account_name).checked;

          url = APIURL + "/api/v2/wallet/update_account/";
          payload = JSON.stringify({
            "email": sigbro_alerts_email,
            "session": sigbro_alerts_token,
            "accountRS": account_name,
            "active": active,
            "alert_tx": tx,
            "alert_block": block,
            "alert_approvals" : approvals,
          });

          sendJSON(url, payload, TIMEOUT_SUBMIT, page_alerts_update_account);

          setTimeout(function () {
            button.disabled = false;
          }, 2000);

        });

        // change approvals status
        $(document).on('click', '.sigbro-alerts-checkbox-approvals', function(e) {
          this.disabled = true;
          var button = this;

          var sigbro_alerts_token = localStorage.getItem("sigbro_alerts_token");
          var sigbro_alerts_email = localStorage.getItem("sigbro_alerts_email");
          var account_name = this.id.replace("sigbro_alerts-approvals_", "");

          var active = document.getElementById("sigbro_alerts--active_" + account_name).checked;
          var tx = document.getElementById("sigbro_alerts--transaction_" + account_name).checked;
          var block = document.getElementById("sigbro_alerts--block_" + account_name).checked;
          var approvals = document.getElementById("sigbro_alerts--approvals_" + account_name).checked;

          url = APIURL + "/api/v2/wallet/update_account/";
          payload = JSON.stringify({
            "email": sigbro_alerts_email,
            "session": sigbro_alerts_token,
            "accountRS": account_name,
            "active": active,
            "alert_tx": tx,
            "alert_block": block,
            "alert_approvals" : approvals,
          });

          sendJSON(url, payload, TIMEOUT_SUBMIT, page_alerts_update_account);


          setTimeout(function () {
            button.disabled = false;
          }, 2000);

        });

        // change active status
        $(document).on('click', '.sigbro-alerts-checkbox-active', function(e) {
          this.disabled = true;
          var button = this;

          var sigbro_alerts_token = localStorage.getItem("sigbro_alerts_token");
          var sigbro_alerts_email = localStorage.getItem("sigbro_alerts_email");
          var account_name = this.id.replace("sigbro_alerts--active_", "");

          var active = document.getElementById("sigbro_alerts--active_" + account_name).checked;
          var tx = document.getElementById("sigbro_alerts--transaction_" + account_name).checked;
          var block = document.getElementById("sigbro_alerts--block_" + account_name).checked;
          var approvals = document.getElementById("sigbro_alerts--approvals_" + account_name).checked;

          url = APIURL + "/api/v2/wallet/update_account/";
          payload = JSON.stringify({
            "email": sigbro_alerts_email,
            "session": sigbro_alerts_token,
            "accountRS": account_name,
            "active": active,
            "alert_tx": tx,
            "alert_block": block,
            "alert_approvals" : approvals,
          });

          sendJSON(url, payload, TIMEOUT_SUBMIT, page_alerts_update_account);

          setTimeout(function () {
            button.disabled = false;
            page_alerts_get_accounts();
            page_alerts_get_inactive_accounts();
          }, 1000);

        });

        $(document).on('click', '.sigbro-alerts-remove-button', function (e) {
          e.preventDefault();
          var button = this;
          button.disabled = true;

          //console.log(button);

          var sigbro_alerts_token = localStorage.getItem("sigbro_alerts_token");
          var sigbro_alerts_email = localStorage.getItem("sigbro_alerts_email");

          var account_name = button.id.replace("sigbro_alerts--remove_", "");

          url = APIURL + "/api/v2/wallet/remove_account/";
          payload = JSON.stringify({
            "email": sigbro_alerts_email,
            "session": sigbro_alerts_token,
            "accountRS": account_name
          });

          //console.log(payload);

          sendJSON(url, payload, TIMEOUT_SUBMIT, page_alerts_remove_account);
          setTimeout(function () {
            button.disabled = false;
          }, 6000);

        });



      }
    });

  } else if (sigbro_alerts_email && !sigbro_alerts_token) {
    $.ajax({
      url: 'alerts_pin.html?_' + new Date().getTime(),
      type: 'GET',
      dataType: 'text',

      success: function (response) {
        $('#sigbro_spa').html(response);
        page_show_network_type();
        document.getElementById('sigbro_alerts--user_email').value = sigbro_alerts_email;
      },

      error: function (error) {
        //console.log('ERROR: ', error);
      },

      complete: function (xhr, status) {

        function validateEmail(email) {
          var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
          return re.test(String(email).toLowerCase());
        }

        // alerts // LOGIN CLICK
        $(document).on('click', '#sigbro_alerts--button_submit_PIN', function (e) {
          e.preventDefault();
          document.getElementById('sigbro_alerts--button_submit_PIN').disabled = true;

          var email = document.getElementById('sigbro_alerts--user_email').value;
          var is_valid = validateEmail(email);
          if (!is_valid) {
            page_alerts_show_alert("Email is not correct.");
            setTimeout(function () {
              document.getElementById('sigbro_alerts--button_submit_PIN').disabled = false;
              page_alerts_hide_alert();
            }, 2000);
          } else {

            // checking PIN
            var pin = document.getElementById('sigbro_alerts--user_PIN').value;

            if (pin.length == 0) {

              page_alerts_show_alert("Check you mail and enter PIN code.");
              setTimeout(function () {
                document.getElementById('sigbro_alerts--button_submit_PIN').disabled = false;
                page_alerts_hide_alert();
              }, 2000);

            } else {
              payload = JSON.stringify(
                {
                  "email": email,
                  "pin": pin
                }
              );
              url = APIURL + "/api/v2/wallet/checkpin/";

              sendJSON(url, payload, TIMEOUT_SUBMIT, page_alerts_check_pincode)

            }

          }
        });





      }
    });

  } else {
    $.ajax({
      url: 'alerts_login.html?_' + new Date().getTime(),
      type: 'GET',
      dataType: 'text',

      success: function (response) {
        $('#sigbro_spa').html(response);
        page_show_network_type();
      },

      error: function (error) {
        //console.log('ERROR: ', error);
      },

      complete: function (xhr, status) {

        function validateEmail(email) {
          var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
          return re.test(String(email).toLowerCase());
        }

        // alerts // send pin CLICK
        $(document).on('click', '#sigbro_alerts--button_submit_email', function (e) {
          e.preventDefault();
          document.getElementById('sigbro_alerts--button_submit_email').disabled = true;

          var email = document.getElementById('sigbro_alerts--user_email').value;
          var is_valid = validateEmail(email);
          if (!is_valid) {
            page_alerts_show_alert("Email is not correct.");
            setTimeout(function () {
              document.getElementById('sigbro_alerts--button_submit_email').disabled = false;
              page_alerts_hide_alert();
            }, 5000);
          } else {

            payload = JSON.stringify({ "email": email });
            url = APIURL + "/api/v2/wallet/sendpin/";

            var is_mail_send = localStorage.getItem("sigbro_alerts_mail_send");

            if (is_mail_send) {

            } else {
              sendJSON(url, payload, TIMEOUT_SUBMIT, page_alerts_show_pincode);
              localStorage.setItem("sigbro_alerts_mail_send", "ok");
              setTimeout(function () {
                localStorage.removeItem("sigbro_alerts_mail_send");
              }, 5000);
            }


          }
        });

      }

    });

  }

}

function page_alerts_add_account() {
  var resp = this.responseText;

  if (resp) {
    var resp_j = JSON.parse(resp);

    //console.log(resp_j);

    if (resp_j.result && resp_j.result == "ok") {
      show_alerts();

    } else {
      page_alerts_show_alert(resp_j.msg);
      setTimeout(function () {
        document.getElementById("sigbro_alerts--add_acount").disabled = false;
      }, 2000);
      return false;
    }

    return true;
  }
}

function page_alerts_remove_account() {
  var resp = this.responseText;

  if (resp) {
    var resp_j = JSON.parse(resp);

    //console.log(resp_j);

    if (resp_j.result && resp_j.result == "ok") {
      show_alerts();

    } else {
      page_alerts_show_alert(resp_j.msg);
      setTimeout(function () {
        page_alerts_hide_alert();
      }, 5000);
      return false;
    }

    return true;
  }
}

function page_alerts_update_account() {
  var resp = this.responseText;

  if (resp) {
    var resp_j = JSON.parse(resp);

    //console.log(resp_j);

    if (resp_j.result && resp_j.result == "ok") {
      page_alerts_show_alert("Account updated");
      setTimeout(function () {
        page_alerts_hide_alert();
      }, 500);
      return true;
    } else {
      page_alerts_show_alert(resp_j.msg);
      setTimeout(function () {
        page_alerts_hide_alert();
      }, 2000);
      return false;
    }

    return true;
  }
}

function page_alerts_check_pincode() {
  // response from API after send PIN request
  var resp = this.responseText;
  var resp_j = JSON.parse(resp);

  //console.log("RESULT:");
  //console.log(resp_j);

  if (resp_j.result && resp_j.result == "fail") {
    // clear email and reload page
    localStorage.removeItem("sigbro_alerts_email");
    page_alerts_show_alert(resp_j.msg);
    setTimeout(function () {
      show_alerts();
    }, 2000);

    return true;
  }
  if (resp_j.result && resp_j.result == "retry") {
    page_alerts_show_alert(resp_j.msg);
    setTimeout(function () {
      show_alerts();
    }, 2000);
    return true;
  } else {
    // save session
    if (resp_j.session) {
      localStorage.setItem("sigbro_alerts_token", resp_j.session);
      show_alerts();
    }

  }

}


function page_alerts_show_pincode() {
  // response from API after send PIN request
  var resp = this.responseText;
  var resp_j = JSON.parse(resp);

  //console.log("RESULT:");
  //console.log(resp_j);

  if (resp_j.result && resp_j.result == "fail") {
    page_alerts_show_alert(resp_j.msg);

  } else {
    localStorage.setItem("sigbro_alerts_email", resp_j.email);
    show_alerts();
  }

}

function show_qr(is_template) {
  $.ajax({
    url: 'qr.html?_' + new Date().getTime(),
    type: 'GET',
    dataType: 'text',

    success: function (response) {
      // show page
      $('#sigbro_spa').html(response);
      // load data
      page_show_network_type();
      page_qr_show_qrcode(is_template);
      page_qr_set_right_color();
    },

    error: function (error) {
      //console.log('ERROR: ', error);
    },

    complete: function (xhr, status) {
      //console.log('DONE');
    }
  });

}

function show_offline_page() {
  $.ajax({
    url: 'offline.html?_' + new Date().getTime(),
    type: 'GET',
    dataType: 'text',

    success: function (response) {
      // show page
      $('#sigbro_spa').html(response);
      // load data
      page_show_network_type();
    },

    error: function (error) {
      //console.log('ERROR: ', error);
    },

    complete: function (xhr, status) {
      //console.log('DONE');
      $(document).on('click', '#sigbro_offline--broadcast', function (e) {
        e.preventDefault();
        var bytes = document.getElementById('sigbro_offline--signed_bytes').value;
        var url = _get_network_url('ardor');

        var param = "requestType=broadcastTransaction&transactionBytes=" + bytes;
        sendPOST(url, param, TIMEOUT_SUBMIT, page_offline_show_broadcast_result);
        return;
      });

    }
  });
}

function page_offline_show_broadcast_result() {
  var resp = this.responseText;
  var resp_j = JSON.parse(resp);

  console.log("BROADCAST RESULT:");
  console.log(resp_j);

  if (resp_j.errorDescription) {
    page_offline_show_alert(resp_j.errorDescription);
  } else if (resp_j.fullHash) {
    page_offline_show_alert("Success: " + resp_j.fullHash);
  }
}

function show_operations() {
  $.ajax({
    url: 'operations.html?_' + new Date().getTime(),
    type: 'GET',
    dataType: 'text',

    success: function (response) {
      // show page
      $('#sigbro_spa').html(response);
      // load data
      page_show_network_type();
      page_ops_set_accountRS();
    },

    error: function (error) {
      //console.log('ERROR: ', error);
    },

    complete: function (xhr, status) {
      //console.log('DONE');
    }
  });
}

function show_profile() {
  $.ajax({
    url: 'profile.html?_' + new Date().getTime(),
    type: 'GET',
    dataType: 'text',

    success: function (response) {
      // show page
      $('#sigbro_spa').html(response);
      // load data
      page_show_network_type();
      page_profile_set_accountRS();
      page_profile_set_userinfo();
      page_profile_show_public_key_alert();

    },

    error: function (error) {
      //console.log('ERROR: ', error);
    },

    complete: function (xhr, status) {
      //console.log('DONE');
    }
  });



}

function show_balances() {

  $.ajax({
    url: 'balances.html?_' + new Date().getTime(),
    type: 'GET',
    dataType: 'text',

    success: function (response) {
      // show page
      $('#sigbro_spa').html(response);
      // load data
      page_show_network_type();
      page_balances_set_accountRS();
      //page_balances_set_userinfo();

      page_balances_show_balance_ardor();
      page_balances_show_assets();
      page_balances_show_currencies();
    },

    error: function (error) {
      //console.log('ERROR: ', error);
    },

    complete: function (xhr, status) {
      //console.log('DONE');
    }
  });



}

function show_index() {
  $.ajax({
    url: 'main.html?_' + new Date().getTime(),
    type: 'GET',
    dataType: 'text',

    success: function (response) {
      // show page
      $('#sigbro_spa').html(response);

      // autofill
      var accAUTO = localStorage.getItem("sigbro_wallet_autologin");
      $('#sigbro_index-input-account').val(accAUTO);
    },

    error: function (error) {
      //console.log('ERROR: ', error);
    },

    complete: function (xhr, status) {

      // index // LOG IN CLICK
      $(document).on('click', '#sigbro_index-button-login', function (e) {
        e.preventDefault();
        var accRS = $('#sigbro_index-input-account').val();
        //console.log(accRS);
        // ARDOR-ZZZZ-48G3-9F9W-4CLJZ
        var ardorRegex = /^ARDOR-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{5}/ig
        var nxtRegex = /^NXT-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{5}/ig

        if (ardorRegex.test(accRS) || nxtRegex.test(accRS)) {
          localStorage.setItem("sigbro_wallet_accountRS", accRS);
          getPublicKey_v2(accRS, 'ardor');
          if (document.getElementById('sigbro_index-rememberme').checked) {
            // save account 
            localStorage.setItem("sigbro_wallet_autologin", accRS);
          }

          localStorage.setItem("sigbro_wallet_page", "balances");
          show_balances();
        } else {
          alert("Check your accountRS and try again.");
        }
      });
    }
  });

}

function show_auth() {
  $.ajax({
    url: 'auth.html?_' + new Date().getTime(),
    type: 'GET',
    dataType: 'text',

    success: function (response) {
      // show page
      $('#sigbro_spa').html(response);
    },
    error: function (error) {
      //console.log('ERROR: ', error);
    },
    complete: function (xhr, status) {
      // generate QR code
      page_qr_show_qrcode_for_auth();
      // TODO:  Start timer for asking backend about login
    }
  });
}


/////////////////////////////////// OPERATIONS
function page_ops_show_alert(msg) {
  var msg_block = document.getElementById('sigbro_send_messages_block');
  msg_block.setAttribute('style', 'display:none;');
  document.getElementById('sigbro_send_messages_text').innerHTML = msg;
  msg_block.setAttribute('style', '');
}

function page_ops_set_accountRS() {
  var accRS = localStorage.getItem("sigbro_wallet_accountRS");
  if (accRS == null) { sigbro_clear_localstorage(); location.href = "/index.html"; }
  document.getElementById('sigbro_send_senderRS').value = accRS;
  document.getElementById('sigbro_template_recipientRS').value = accRS;

  var senderPubKey = localStorage.getItem("sigbro_pubkey_" + accRS);
  if (senderPubKey == null) {
    getPublicKey_v2(accRS, 'ardor');
  }

}

// template generator click
/*
template = {
    'network' : 'test',
    'chain' : 2, # ignis
    'requestType' : 'sendMoney',
    'recipientRS' : 'ARDOR-NYJW-6M4F-6LG2-76FR5',
    'amountNQT' : 1000000000,
    'message' : 'I love you, Sigbro Mobile'
  }
*/
$(document).on('click', '#sigbro_template_submit', function (e) {
  var msg_block = document.getElementById('sigbro_template_messages_block');
  msg_block.setAttribute('style', 'display:none;');

  var recipientRS = document.getElementById('sigbro_template_recipientRS').value;
  var currencie = document.getElementById('sigbro_template_currencie').value;
  var operation = document.getElementById('sigbro_template_operation').value;

  var url = TEMPLATEURL + "/api/v1/add/";

  var _network = localStorage.getItem("sigbro_wallet_network");
  if (_network == 'mainnet') {
    NETWORK = "main";
  } else {
    NETWORK = "test";
  }

  if (operation == 'sendMoney') {
    var amount = document.getElementById('sigbro_template_amount').value;
    var msg = document.getElementById('sigbro_template_message').value;

    template = {
      "network": NETWORK,
      "chain": currencie,
      "requestType": operation,
      "recipientRS": recipientRS,
      "amount": amount,
      "message": msg
    };

  }

  if (operation == 'leaseBalance') {
    var period = document.getElementById('sigbro_template_lease_period').value;

    template = {
      "network": NETWORK,
      "chain": currencie,
      "requestType": operation,
      "recipientRS": recipientRS,
      "period": period
    };

  }



  param = JSON.stringify(
    { "template": template }
  );

  //console.log("url: " + url);
  //console.log("params: " + param);

  sendJSON(url, param, TIMEOUT_TEMPLATE, page_ops_template_show_result);
});

// template operator response
function page_ops_template_show_result() {
  var resp = this.responseText;
  var resp_j = JSON.parse(resp);

  //console.log("RESULT:");
  //console.log(resp_j);

  if (resp_j.error) {
    page_ops_show_alert(resp_j.error);
  } else if (resp_j.uuid) {
    var resp_url = "https://sigbro-template.api.nxter.org/api/v1/get/" + resp_j.uuid + "/";
    //console.log("URL: " + resp_url);
    localStorage.setItem("sigbro_wallet_url", resp_url);
    show_qr(true);
  }
}



$(document).on('click', '#sigbro_send_submit', function (e) {
  var msg_block = document.getElementById('sigbro_send_messages_block');
  msg_block.setAttribute('style', 'display:none;');

  var senderRS = document.getElementById('sigbro_send_senderRS').value;

  var senderPubKey = localStorage.getItem("sigbro_pubkey_" + senderRS);

  if (senderPubKey == null) {
    page_ops_show_alert("Your account does not have PublicKey. You cannot send any transaction with SIGBRO WALLET, sorry");
    return;
  }

  // check recipient publicKey
  var recipientRS = document.getElementById('sigbro_send_recipientRS').value;
  getPublicKey_v2(recipientRS, 'ardor')
  var recipientPublicKey = localStorage.getItem("sigbro_pubkey_" + recipientRS)

  if (recipientPublicKey == null) {
    recipientPublicKey = prompt("Recipient accountRS does not have a publicKey, please provide:")
  }

  if (recipientPublicKey == null) {
    page_ops_show_alert("You cannot send money to the accountRS without PublicKey.");
    return;
  }

  var amount = document.getElementById('sigbro_send_amount').value;
  var fee = -1;

  var encrypt_msg = 0;

  var currencie = document.querySelector('input[name = "sigbro_send_selector"]:checked').value;
  var msg = document.getElementById('sigbro_send_message').value;


  var url = APIURL + "/api/v2/sendmoney/" + _get_network_prefix() + "/";

  param_json = {
    "currencie": currencie,
    "recipient": recipientRS,
    "amount": amount,
    "publicKey": senderPubKey,
    "fee": fee,
    "msg": msg,
    "encrypt_msg": encrypt_msg,
    "recipientPublicKey": recipientPublicKey
  };
  param = JSON.stringify(param_json);

  //console.log("url: " + url);
  //console.log("params: " + param);

  sendJSON(url, param, TIMEOUT_SUBMIT, page_ops_show_result);
});


function page_ops_show_result() {
  var resp = this.responseText;
  var resp_j = JSON.parse(resp);

  //console.log("RESULT:");
  //console.log(resp_j);

  if (resp_j.error) {
    page_ops_show_alert(resp_j.error);
    //alert ( resp_j.error ); 
  } else if (resp_j.url) {
    //console.log("URL: " + resp_j.url);
    localStorage.setItem("sigbro_wallet_url", resp_j.url);
    show_qr(false);
  }
}

/////////////////////////////////// QR
function page_qr_show_qrcode(is_template) {
  var accURL = localStorage.getItem("sigbro_wallet_url");

  if (accURL == null) {
    return;
  }

  if (is_template == false) {
    var link = document.getElementById("sigbro_qr-url");
    link.textContent = "Show transaction details in browser.";
    link.setAttribute("href", accURL);
  } else {

  }

  var sigbroURL = accURL.replace("https", "sigbro");
  var link_sigbro = document.getElementById("sigbro_qr--mobile_url");
  link_sigbro.setAttribute("href", sigbroURL);

  var QRC = qrcodegen.QrCode;
  var qr0 = QRC.encodeText(accURL, QRC.Ecc.HIGH);

  var code = qr0.toSvgString(4);
  var svg = document.getElementById("sigbro_qr-qrcode");

  svg.setAttribute("viewBox", / viewBox="([^"]*)"/.exec(code)[1]);
  svg.querySelector("path").setAttribute("d", / d="([^"]*)"/.exec(code)[1]);
  svg.style.removeProperty("display");
}

///////////////////////////////// SHOW QR ON AUTH PAGE
function page_qr_show_qrcode_for_auth() {
  try {
    var sigbroUUID = JSON.parse(localStorage.getItem("sigbro_uuid"));
  } catch (err) {
    return;
  }
  if (sigbroUUID == null) {
    return;
  }

  var uuid = sigbroUUID.uuid;
  var url = "sigbro://" + uuid;
  //console.log(url);

  var QRC = qrcodegen.QrCode;
  var qr0 = QRC.encodeText(url, QRC.Ecc.HIGH);
  var code = qr0.toSvgString(4);

  var svg = document.getElementById("sigbro_auth--qr_code_sigbromobile");
  svg.setAttribute("viewBox", / viewBox="([^"]*)"/.exec(code)[1]);
  svg.querySelector("path").setAttribute("d", / d="([^"]*)"/.exec(code)[1]);
  svg.style.removeProperty("display");
}



/////////////////////////////////// BALANCES

// save assets info
function page_balances_save_assets() {
  var resp = this.responseText;
  var respJSON = JSON.parse(resp);
  // //console.log(respJSON);

  if (respJSON.data) {
    var timestamp = Date.now();
    var tmp = { 'value': respJSON.data, 'timestamp': timestamp };
    localStorage.setItem('sigbro_wallet_assets', JSON.stringify(tmp));

    page_balances_show_assets();
  } else {
    //console.log(respJSON);
  }

}

//show assets
function page_balances_show_assets() {
  var accRS = localStorage.getItem("sigbro_wallet_accountRS");
  var assets = localStorage.getItem("sigbro_wallet_assets");

  if (assets == null) {
    var url = APIURL + "/api/v2/assets/" + accRS + "/en/" + _get_network_prefix() + "/";
    getJSON(url, TIMEOUT_ARDR, page_balances_save_assets, "assets");
    return;
  }

  assets_data = JSON.parse(assets);

  // If delta > 5 min need to get new balances
  var delta = Date.now() - assets_data.timestamp;
  //console.log("Delta: " + delta / 1000 + " sec.");
  if (delta > 5 * 60 * 1000) {
    var url = APIURL + "/api/v2/assets/" + accRS + "/en/" + _get_network_prefix() + "/";
    getJSON(url, TIMEOUT_ARDR, page_balances_save_assets, "assets");
    return;
  }
  if (document.getElementById('sigbro_wallet_assets')) {
    document.getElementById('sigbro_wallet_assets').innerHTML = assets_data.value;
  }
}

// save currencies
function page_balances_save_currencies() {
  var resp = this.responseText;
  var respJSON = JSON.parse(resp);
  // //console.log(respJSON);

  if (respJSON.data) {
    var timestamp = Date.now();
    var tmp = { 'value': respJSON.data, 'timestamp': timestamp };
    localStorage.setItem('sigbro_wallet_currencies', JSON.stringify(tmp));

    page_balances_show_currencies();
  } else {
    //console.log(respJSON);
  }

}

function page_balances_show_currencies() {
  var accRS = localStorage.getItem("sigbro_wallet_accountRS");
  var currencies = localStorage.getItem("sigbro_wallet_currencies");

  if (currencies == null) {
    var url = APIURL + "/api/v2/currencies/" + accRS + "/en/" + _get_network_prefix() + "/";
    getJSON(url, TIMEOUT_ARDR, page_balances_save_currencies, "currencies");
    return;
  }

  curr_data = JSON.parse(currencies);

  // If delta > 5 min need to get new balances
  var delta = Date.now() - curr_data.timestamp;
  //console.log("Delta: " + delta / 1000 + " sec.");
  if (delta > 5 * 60 * 1000) {
    var url = APIURL + "/api/v2/currencies/" + accRS + "/en/" + _get_network_prefix() + "/";
    getJSON(url, TIMEOUT_ARDR, page_balances_save_currencies, "currencies");
    return;
  }

  if (document.getElementById('sigbro_wallet_currencies')) {
    document.getElementById('sigbro_wallet_currencies').innerHTML = curr_data.value;
  }

}

////////////////////////////////// profile
function page_profile_set_accountRS() {
  var accRS = localStorage.getItem("sigbro_wallet_accountRS");
  if (accRS == null) { sigbro_clear_localstorage(); location.href = "/index.html"; }

  document.getElementById('sigbro_profile-accountRS').textContent = accRS;
}

// callback function for userinf
function page_profile_save_userinfo(data) {
  var resp = this.responseText;

  var respJSON = JSON.parse(resp);

  if (respJSON.name) {
    localStorage.setItem('sigbro_wallet_username', respJSON.name);
  } else {
    localStorage.setItem('sigbro_wallet_username', 'NoName');
  }

  if (respJSON.description) {
    localStorage.setItem('sigbro_wallet_userdesc', respJSON.description);
  } else {
    localStorage.setItem('sigbro_wallet_userdesc', '');
  }

  page_profile_set_userinfo();
}

function page_profile_show_public_key_alert() {
  // show alert if user does not have public key
  var accRS = localStorage.getItem("sigbro_wallet_accountRS");
  var pubKey = localStorage.getItem("sigbro_pubkey_" + accRS);

  if (pubKey == null) {
    document.getElementById('sigbro_profile-username').textContent = "WARNING!";
    document.getElementById('sigbro_profile--warning').textContent = "Your account does not have a public key. It is recommended to register new accounts by sending an outgoing transaction OR announcing its public key from another account or a faucet.";
  }
}

function page_profile_set_userinfo() {
  // get username from localstorage
  var accRS = localStorage.getItem("sigbro_wallet_accountRS");
  var accName = localStorage.getItem('sigbro_wallet_username');
  var accDesc = localStorage.getItem('sigbro_wallet_userdesc');

  if (accName == null || accDesc == null) {
    // need to get info from blockchain
    var url = _get_network_url('ardor') + "?requestType=getAccount&account=" + accRS;
    getJSON(url, TIMEOUT_ARDR, page_profile_save_userinfo, "");
    return;
  }

  document.getElementById('sigbro_profile-username').textContent = accName;
  document.getElementById('sigbro_profile-userdesc').textContent = accDesc;
}


/////////////////////////////////// balances

function page_balances_set_accountRS() {
  var accRS = localStorage.getItem("sigbro_wallet_accountRS");
  if (accRS == null) { sigbro_clear_localstorage(); location.href = "/index.html"; }

  document.getElementById('sigbro_balances-accountRS').textContent = accRS;
}

// callback function for userinf
function page_balances_save_userinfo(data) {
  var resp = this.responseText;

  var respJSON = JSON.parse(resp);

  if (respJSON.name) {
    localStorage.setItem('sigbro_wallet_username', respJSON.name);
  } else {
    localStorage.setItem('sigbro_wallet_username', 'NoName');
  }

  if (respJSON.description) {
    localStorage.setItem('sigbro_wallet_userdesc', respJSON.description);
  } else {
    localStorage.setItem('sigbro_wallet_userdesc', '');
  }

  page_balances_set_userinfo();
}

function page_balances_set_userinfo() {
  // get username from localstorage
  var accRS = localStorage.getItem("sigbro_wallet_accountRS");
  var accName = localStorage.getItem('sigbro_wallet_username');
  var accDesc = localStorage.getItem('sigbro_wallet_userdesc');

  if (accName == null || accDesc == null) {
    // need to get info from blockchain
    var url = _get_network_url('ardor') + "?requestType=getAccount&account=" + accRS;
    getJSON(url, TIMEOUT_ARDR, page_balances_save_userinfo, "custom text");
    return;
  }

  document.getElementById('sigbro_balances-username').textContent = accName;
  document.getElementById('sigbro_balances-userdesc').textContent = accDesc;

}

// callback function for ARDOR balance
function page_balances_set_balance_ardor(data) {
  var resp = this.responseText;
  var respJSON = JSON.parse(resp);
  //console.log(respJSON);

  if (respJSON.balances) {
    // get correct response
    var timestamp = Date.now();
    var ardor = respJSON.balances[1].balanceNQT / Math.pow(10, 8);
    var ignis = respJSON.balances[2].balanceNQT / Math.pow(10, 8);
    var aeur = respJSON.balances[3].balanceNQT / Math.pow(10, 4);
    var bitswift = respJSON.balances[4].balanceNQT / Math.pow(10, 8);
    var mpg = respJSON.balances[5].balanceNQT / Math.pow(10, 8);

    var tmp = { 'value': ardor, 'timestamp': timestamp };
    localStorage.setItem('sigbro_wallet_balance_ardor', JSON.stringify(tmp));

    var tmp = { 'value': ignis, 'timestamp': timestamp };
    localStorage.setItem('sigbro_wallet_balance_ignis', JSON.stringify(tmp));

    var tmp = { 'value': aeur, 'timestamp': timestamp };
    localStorage.setItem('sigbro_wallet_balance_aeur', JSON.stringify(tmp));

    var tmp = { 'value': bitswift, 'timestamp': timestamp };
    localStorage.setItem('sigbro_wallet_balance_bitswift', JSON.stringify(tmp));

    var tmp = { 'value': mpg, 'timestamp': timestamp };
    localStorage.setItem('sigbro_wallet_balance_mpg', JSON.stringify(tmp));

    page_balances_show_balance_ardor()
  } else {
    document.getElementById('sigbro_balances-balance-ardor').textContent = "NaN";
    document.getElementById('sigbro_balances-balance-ignis').textContent = "NaN";
    document.getElementById('sigbro_balances-balance-aeur').textContent = "NaN";
    document.getElementById('sigbro_balances-balance-bitswift').textContent = "NaN";
    document.getElementById('sigbro_balances-balance-mpg').textContent = "NaN";
    //console.log(respJSON);
  }

}

function number_pretty_print(x) {
  var parts = x.toString().split(".");
  parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, " ");
  return parts.join(".");
}

// set ardor, ignis, aeur, bitswift balance on the page
function page_balances_show_balance_ardor() {
  var accRS = localStorage.getItem("sigbro_wallet_accountRS");
  var accBalanceArdor = localStorage.getItem('sigbro_wallet_balance_ardor');
  var accBalanceIgnis = localStorage.getItem('sigbro_wallet_balance_ignis');
  var accBalanceAeur = localStorage.getItem('sigbro_wallet_balance_aeur');
  var accBalanceBitswift = localStorage.getItem('sigbro_wallet_balance_bitswift');
  var accBalanceMPG = localStorage.getItem('sigbro_wallet_balance_mpg');

  if (accBalanceArdor == null || accBalanceIgnis == null || accBalanceAeur == null || accBalanceBitswift == null || accBalanceMPG == null) {
    var url = _get_network_url('ardor') + "?requestType=getBalances&account=" + accRS + "&chain=1&chain=2&chain=3&chain=4&chain=5";
    getJSON(url, TIMEOUT_ARDR, page_balances_set_balance_ardor, "balance ARDOR");
    return;
  }

  accBalanceArdor = JSON.parse(accBalanceArdor);
  accBalanceIgnis = JSON.parse(accBalanceIgnis);
  accBalanceAeur = JSON.parse(accBalanceAeur);
  accBalanceBitswift = JSON.parse(accBalanceBitswift);
  accBalanceMPG = JSON.parse(accBalanceMPG);


  // If delta > 5 min need to get new balances
  var delta = Date.now() - accBalanceArdor.timestamp;
  //console.log("Delta: " + delta / 1000 + " sec.");
  if (delta > 5 * 60 * 1000) {
    var url = _get_network_url('ardor') + "?requestType=getBalances&account=" + accRS + "&chain=1&chain=2&chain=3&chain=4&chain=5";
    getJSON(url, TIMEOUT_ARDR, page_balances_set_balance_ardor, "balance ARDOR");
    return;
  }

  document.getElementById('sigbro_balances-balance-ardor').textContent = number_pretty_print(accBalanceArdor.value);
  document.getElementById('sigbro_balances-balance-ignis').textContent = number_pretty_print(accBalanceIgnis.value);
  document.getElementById('sigbro_balances-balance-aeur').textContent = number_pretty_print(accBalanceAeur.value);
  document.getElementById('sigbro_balances-balance-bitswift').textContent = number_pretty_print(accBalanceBitswift.value);
  document.getElementById('sigbro_balances-balance-mpg').textContent = number_pretty_print(accBalanceMPG.value);

}


////////////////////////////////////////////////////////////////////// 

function sigbro_clear_localstorage() {
  // remove all data from local storage. it used when somebody click on logout and when we don't find accountRS 
  localStorage.removeItem("sigbro_wallet_accountRS");
  localStorage.removeItem("sigbro_wallet_username");
  localStorage.removeItem("sigbro_wallet_userdesc");
  localStorage.removeItem("sigbro_wallet_page");

  localStorage.removeItem("sigbro_wallet_assets");
  localStorage.removeItem("sigbro_wallet_currencies");

  localStorage.removeItem("sigbro_wallet_balance_aeur");
  localStorage.removeItem("sigbro_wallet_balance_ardor");
  localStorage.removeItem("sigbro_wallet_balance_ignis");
  localStorage.removeItem("sigbro_wallet_balance_bitswift");

  localStorage.removeItem("sigbro_wallet_url"); // last created url
  localStorage.removeItem("sigbro_uuid"); // uuid from last logon

  localStorage.removeItem("sigbro_alerts_cache_inactive_accounts"); // clear cache of the page
  localStorage.removeItem("sigbro_alerts_cache_active_accounts"); // clear cache of the page
}

function sigbro_clear_balances() {
  localStorage.removeItem("sigbro_wallet_assets");
  localStorage.removeItem("sigbro_wallet_currencies");

  localStorage.removeItem("sigbro_wallet_balance_aeur");
  localStorage.removeItem("sigbro_wallet_balance_ardor");
  localStorage.removeItem("sigbro_wallet_balance_ignis");
  localStorage.removeItem("sigbro_wallet_balance_bitswift");

  localStorage.removeItem("sigbro_wallet_url"); // last created url
  localStorage.removeItem("sigbro_uuid"); // uuid from last logon
}

$(document).on('click', '#sigbro-logout', function (e) {
  e.preventDefault();
  localStorage.setItem("sigbro_wallet_page", "index");
  sigbro_clear_localstorage();
  show_index();
});

$(document).on('click', '#sigbro_alerts--logout', function (e) {
  e.preventDefault();
  localStorage.removeItem("sigbro_alerts_email");
  localStorage.removeItem("sigbro_alerts_token")
  show_alerts();
});



$(document).on('click', '#sigbro-change-network', function (e) {
  e.preventDefault();

  var network = localStorage.getItem("sigbro_wallet_network");
  if (network == null) {
    localStorage.setItem("sigbro_wallet_network", "testnet");
    network = "testnet";
  }
  if (network == 'mainnet') {
    localStorage.setItem("sigbro_wallet_network", "testnet");
  } else {
    localStorage.setItem("sigbro_wallet_network", "mainnet");
  }

  sigbro_clear_balances();
  location.reload();
});

// change auth type: accountRS or SIGBRO MOBILE
$(document).on('click', '#sigbo_index--btn_auth_accountrs', function (e) {
  e.preventDefault();

  var accountrs_block = document.getElementById('sigbro_index--auth_accountrs');
  var sigbro_block = document.getElementById('sigbro_index--auth_sigbro');
  var remember_me = document.getElementById('sigbro_index--remember_me');

  sigbro_block.setAttribute('style', 'display:none;');
  accountrs_block.setAttribute('style', '');
  remember_me.setAttribute('style', '');

  document.getElementById('sigbo_index--btn_auth_accountrs').classList.add('active');
  document.getElementById('sigbo_index--btn_auth_sigbro').classList.remove('active');
});

$(document).on('click', '#sigbo_index--btn_auth_sigbro', function (e) {
  e.preventDefault();

  var accountrs_block = document.getElementById('sigbro_index--auth_accountrs');
  var sigbro_block = document.getElementById('sigbro_index--auth_sigbro');
  var remember_me = document.getElementById('sigbro_index--remember_me');

  accountrs_block.setAttribute('style', 'display:none;');
  remember_me.setAttribute('style', 'display:none;');
  sigbro_block.setAttribute('style', '');

  document.getElementById('sigbo_index--btn_auth_accountrs').classList.remove('active');
  document.getElementById('sigbo_index--btn_auth_sigbro').classList.add('active');

});

function add_new_uuid_result() {
  var resp = this.responseText;
  var resp_j = JSON.parse(resp);

  //console.log(resp_j);
}

// click on OPEN SIGBRO MOBILE
$(document).on('click', '#sigbo_index--btn_open_sigbro_mobile', function (e) {
  e.preventDefault();

  var timestamp = Date.now();
  var old_timestamp = 0;
  var old_uuid = "";
  var uuid = "";

  //TODO: Get uuid from localstorage and check time, if more than 15 min update uuid
  try {
    var uuid_from_localstorage = JSON.parse(localStorage.getItem("sigbro_uuid"));
    old_timestamp = uuid_from_localstorage.timestamp;
    old_uuid = uuid_from_localstorage.uuid;
  } catch (err) {
    //console.log("Incorrect json in localstorage");
  }

  //console.log("Delta: " + (timestamp - old_timestamp));

  if (timestamp - old_timestamp < 15 * 60 * 1000) {
    uuid = old_uuid;
    //console.log("Using old UUID: " + uuid);
  } else {
    uuid = uuidv4();
    //console.log("Using new UUID: " + uuid);

    var uuid_timestamp = { "uuid": uuid, "timestamp": timestamp }
    localStorage.setItem("sigbro_uuid", JSON.stringify(uuid_timestamp));

    // if uuid is new, send it to our API
    url = "https://random.nxter.org/api/auth/new";

    param_json = { "uuid": uuid };
    param = JSON.stringify(param_json);

    sendJSON(url, param, TIMEOUT_ARDR, add_new_uuid_result);
  }

  var source = new EventSource('https://random.nxter.org:9040/stream');

  // subscribe to global events from auth-sse
  source.addEventListener('greeting', function (event) {
    //console.log('Gloabal event');
    var data = JSON.parse(event.data);
    //console.log(data);
    //console.log(event);
  }, false);

  // subscribe to personal events from auth-sse
  source.addEventListener(uuid, function (event) {
    var data = JSON.parse(event.data);

    try {
      var data2 = JSON.parse(data);
    } catch (err) {
      var data2 = data;
    }

    //console.log(data2);

    if (data2.type == 'success' && data2.accountRS) {
      localStorage.setItem("sigbro_wallet_accountRS", data2.accountRS);
      getPublicKey_v2(data2.accountRS, 'ardor');
      localStorage.setItem("sigbro_wallet_page", "balances");
      localStorage.removeItem("sigbro_uuid");
      show_balances();
    } else {
      localStorage.removeItem("sigbro_uuid");
      alert(data2.message);
    }
  }, false);


  // need to open sigbro://UUIDv4 url
  var url_sigbro = "sigbro://" + uuid;
  window.open(url_sigbro, '_blank');

});


// click on show qr code
$(document).on('click', '#sigbo_index--btn_scan_qr_code', function (e) {
  e.preventDefault();

  var timestamp = Date.now();
  var old_timestamp = 0;
  var old_uuid = "";
  var uuid = "";

  //TODO: Get uuid from localstorage and check time, if more than 15 min update uuid
  try {
    var uuid_from_localstorage = JSON.parse(localStorage.getItem("sigbro_uuid"));
    old_timestamp = uuid_from_localstorage.timestamp;
    old_uuid = uuid_from_localstorage.uuid;
  } catch (err) {
    //console.log("Incorrect json in localstorage");
  }

  //console.log("Delta: " + (timestamp - old_timestamp));

  if (timestamp - old_timestamp < 15 * 60 * 1000) {
    uuid = old_uuid;
    //console.log("Using old UUID: " + uuid);
  } else {
    uuid = uuidv4();
    //console.log("Using new UUID: " + uuid);

    var uuid_timestamp = { "uuid": uuid, "timestamp": timestamp }
    localStorage.setItem("sigbro_uuid", JSON.stringify(uuid_timestamp));

    // if uuid is new, send it to our API
    url = "https://random.nxter.org/api/auth/new";

    param_json = { "uuid": uuid };
    param = JSON.stringify(param_json);

    sendJSON(url, param, TIMEOUT_ARDR, add_new_uuid_result);
  }

  show_auth();
  var source = new EventSource('https://random.nxter.org:9040/stream');

  // subscribe to global events from auth-sse
  source.addEventListener('greeting', function (event) {
    //console.log('Gloabal event');
    var data = JSON.parse(event.data);
    //console.log(data);
    //console.log(event);
  }, false);

  // subscribe to personal events from auth-sse
  source.addEventListener(uuid, function (event) {
    var data = JSON.parse(event.data);

    try {
      var data2 = JSON.parse(data);
    } catch (err) {
      var data2 = data;
    }

    //console.log(data2);

    if (data2.type == 'success' && data2.accountRS) {
      localStorage.setItem("sigbro_wallet_accountRS", data2.accountRS);
      getPublicKey_v2(data2.accountRS, 'ardor');
      localStorage.setItem("sigbro_wallet_page", "balances");
      localStorage.removeItem("sigbro_uuid");
      show_balances();
    } else {
      localStorage.removeItem("sigbro_uuid");
      alert(data2.message);
    }
  }, false);


});




// end change auth type: accountRS or SIGBRO MOBILE

function getJSON(url, timeout, callback) {
  var args = Array.prototype.slice.call(arguments, 3);
  var xhr = new XMLHttpRequest();
  xhr.ontimeout = function () {
    //console.log("The request for " + url + " timed out.");
  };
  xhr.onload = function () {
    if (xhr.readyState === 4) {
      if (xhr.status === 200) {
        //console.log('get: ' + url + ' success.');
        callback.apply(xhr, args);
      } else {
        //console.log(xhr.statusText);
      }
    }
  };
  xhr.open("GET", url, true);
  xhr.timeout = timeout;
  xhr.send(null);
}

function sendPOST(url, params, timeout, callback) {
  var args = Array.prototype.slice.call(arguments, 3);
  var xhr = new XMLHttpRequest();
  xhr.ontimeout = function () {
    //console.log("The POST request for " + url + " timed out.");
  };
  xhr.onload = function () {
    if (xhr.readyState === 4) {
      if (xhr.status === 404) {
        //console.log('URL Not Found: ' + url);
        return;
      }

      if (xhr.status === 200) {
        //console.log('post: ' + url + ' success.');
        callback.apply(xhr, args);
      } else {
        //console.log(xhr.statusText);
      }
    }
  };
  xhr.open("POST", url);
  xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
  xhr.timeout = timeout;
  xhr.send(params);
}


function sendJSON(url, params, timeout, callback) {
  var args = Array.prototype.slice.call(arguments, 3);
  var xhr = new XMLHttpRequest();
  xhr.ontimeout = function () {
    //console.log("The POST request for " + url + " timed out.");
  };
  xhr.onload = function () {
    if (xhr.readyState === 4) {
      if (xhr.status === 404) {
        //console.log('URL Not Found: ' + url);
        return;
      }

      if (xhr.status === 200) {
        //console.log('post: ' + url + ' success.');
        callback.apply(xhr, args);
      } else {
        //console.log(xhr.statusText);
      }
    }
  };
  xhr.open("POST", url);
  xhr.setRequestHeader('Content-type', 'application/json');
  xhr.setRequestHeader('X-Sigbro-Wallet', 'sigbro-wallet-web-app');
  xhr.timeout = timeout;
  xhr.send(params);
}

function getPublicKey_v2(accountRS, network) {
  // network = ardor / nxt
  // prefix from localstorage
  var pubKey = localStorage.getItem("sigbro_pubkey_" + accountRS);
  if (pubKey == null) {
    var _network = localStorage.getItem("sigbro_wallet_network");
    if (_network == 'mainnet') {
      _prefix = '';
    } else {
      _prefix = 'tst';
    }

    var url = "https://random.api.nxter.org/" + _prefix + network + "?requestType=getAccountPublicKey&account=" + accountRS;
    getJSON(url, TIMEOUT_ARDR, savePublicKey, accountRS);
  }
}

function savePublicKey(accountRS) {
  // accountRS getting from getJSON additional param (last)
  var resp = this.responseText;
  resp = JSON.parse(resp);

  if (resp.publicKey) {
    localStorage.setItem("sigbro_pubkey_" + accountRS, resp.publicKey);
  }
}


// https://stackoverflow.com/questions/105034/create-guid-uuid-in-javascript
function uuidv4() { // Public Domain/MIT
  var d = new Date().getTime();
  if (typeof performance !== 'undefined' && typeof performance.now === 'function') {
    d += performance.now(); //use high-precision timer if available
  }
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
    var r = (d + Math.random() * 16) % 16 | 0;
    d = Math.floor(d / 16);
    return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
  });
}

function page_qr_set_right_color() {
  // check network type and set backgroud color for logo inside qr-code
  var network = localStorage.getItem("sigbro_wallet_network");
  if (network == null) { localStorage.setItem("sigbro_wallet_network", "testnet"); }
  if (network == 'mainnet') {
    document.getElementById('sigbro_qr--qr_logo').src = "img/sigbro_red.png";
  } else {
    document.getElementById('sigbro_qr--qr_logo').src = "img/sigbro_black.png";
  }
}

function page_show_network_type() {
  // check localstorage for network type and update button
  var network = localStorage.getItem("sigbro_wallet_network");
  //console.log('Network: ' + network)
  if (network == null) {
    localStorage.setItem("sigbro_wallet_network", "testnet");
  }
  if (network == 'mainnet') {
    network = 'mainnet';
    network_caption = 'switch to the testnet';
  } else {
    network = 'testnet';
    network_caption = 'switch to the mainnet';
  }
  document.getElementById('sigbro-change-network').innerHTML = network_caption;
}

function page_alerts_update_header() {
  // check localstorage for email and update header
  var email = localStorage.getItem("sigbro_alerts_email");
  document.getElementById('sigbro_alerts--header').innerHTML = "[ " + email + " ]";
}

function _get_network_url(network) {
  // network = ardor/nxt
  // prefix - from localstorage
  var url = "https://random.api.nxter.org";
  var _network = localStorage.getItem("sigbro_wallet_network");
  if (_network == 'mainnet') {
    url = url + "/" + network;
  } else {
    url = url + "/tst" + network;
  }

  return url;
}

function _get_network_prefix() {
  // return main or test depends on localstorage
  var _network = localStorage.getItem("sigbro_wallet_network");
  if (_network == 'mainnet') {
    return 'main';
  } else {
    return 'test';
  }

  return 'test';
}

function hide_module(name) {
  [].forEach.call(document.querySelectorAll(name), function (el) {
    el.style.visibility = 'hidden';
    el.style.display = 'none';
  });
}

function show_module(name) {
  [].forEach.call(document.querySelectorAll(name), function (el) {
    el.style.visibility = '';
    el.style.display = '';
  });
}

function enable_all_childchain() {
  var list = document.getElementById("sigbro_template_currencie");
  for (var i = 0; i < list.length; i++) {
    list[i].disabled = false;
  }
}

function disable_all_childchain_except(name) {
  var list = document.getElementById("sigbro_template_currencie");
  for (var i = 0; i < list.length; i++) {
    if (list[i].text.toLowerCase() == name.toLowerCase()) {
      list[i].disabled = false;
    } else {
      list[i].disabled = true;
    }
  }
}


function showRightFields() {
  item = document.getElementById("sigbro_template_operation").value;
  //console.log('Selected: ' + item);
  if (item == 'sendMoney') {
    hide_module('.sigbro-module-leasebalance');
    show_module('.sigbro-module-sendmoney');
    enable_all_childchain();
    // set ignis the first
    document.getElementById("sigbro_template_currencie").value = 2;
  }
  if (item == 'leaseBalance') {
    show_module('.sigbro-module-leasebalance');
    hide_module('.sigbro-module-sendmoney');
    // set ardor
    document.getElementById("sigbro_template_currencie").value = 1;
    disable_all_childchain_except('ardor');
  }

}

