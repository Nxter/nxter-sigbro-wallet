// testnet or main net for main functionality
var ARDOR = "https://random.nxter.org/tstardor";
var NXT   = "https://random.nxter.org/tstnxt"; 

// PRODUCTION
var APIURL = "https://sigbro-wallet.api.nxter.org"
var TEMPLATEURL = "https://sigbro-template.api.nxter.org"

// DEVELOPMENT
//var TEMPLATEURL = "http://localhost:9060"
//var APIURL = "http://localhost:8020"

var NETWORK = "test"; // testnet for template functionality
var TIMEOUT = 10000; // timeount for all network operations

$(document).on('click', 'a.nav-link', function(e) {
  e.preventDefault();
  var open_page = $(this).attr('href').replace('#','');

  if ( open_page == 'portfolio' ) { 
    localStorage.setItem("sigbro_wallet_page", "portfolio");
    show_portfolio();
    return;
  }

  if ( open_page == 'profile' ) {
    localStorage.setItem("sigbro_wallet_page", "profile");
    show_profile();
    return;
  }

  if ( open_page == 'operations' ) {
    localStorage.setItem("sigbro_wallet_page", "operations");
    show_operations();
    return;
  }


});

$( document ).ready(function() {
  var page      = localStorage.getItem("sigbro_wallet_page");
  console.log("Last page: " + page);
  if ( page == null ) { page = 'index'; }

  if ( page == 'index' )      { show_index(); return; }
  if ( page == 'profile' )    { show_profile(); return; }
  if ( page == 'portfolio' )  { show_portfolio(); return; }
  if ( page == 'operations' )  { show_operations(); return; }
  
});

function show_qr() {
  $.ajax({ 
    url:        'qr.html',
    type:       'GET',
    dataType:   'text', 

    success: function( response ) {
      // show page
      $('#sigbro_spa').html( response );
      // load data
      page_show_network_type();
      page_qr_show_qrcode();
    },

    error: function ( error ) {
      console.log('ERROR: ', error);
    },

    complete: function( xhr, status ) {
      console.log('DONE');
    }
  });

}

function show_operations() {
  $.ajax({ 
    url:        'operations.html',
    type:       'GET',
    dataType:   'text', 

    success: function( response ) {
      // show page
      $('#sigbro_spa').html( response );
      // load data
      page_show_network_type();
      page_ops_set_accountRS();
    },

    error: function ( error ) {
      console.log('ERROR: ', error);
    },

    complete: function( xhr, status ) {
      console.log('DONE');
    }
  });
}

function show_portfolio() {
  $.ajax({ 
    url:        'portfolio.html',
    type:       'GET',
    dataType:   'text', 

    success: function( response ) {
      // show page
      $('#sigbro_spa').html( response );
      // load data
      page_show_network_type();
      page_portfolio_show_assets();
      page_portfolio_show_currencies();
    },

    error: function ( error ) {
      console.log('ERROR: ', error);
    },

    complete: function( xhr, status ) {
      console.log('DONE');
    }
  });


}


function show_profile() {

  $.ajax({ 
    url:        'profile.html',
    type:       'GET',
    dataType:   'text', 

    success: function( response ) {
      // show page
      $('#sigbro_spa').html( response );
      // load data
      page_show_network_type();
      page_profile_set_accountRS();
      page_profile_set_userinfo();
      page_profile_show_balance_nxt();
      page_profile_show_balance_ardor();
    },

    error: function ( error ) {
      console.log('ERROR: ', error);
    },

    complete: function( xhr, status ) {
      console.log('DONE');
    }
  });



}

function show_index() {
  $.ajax({ 
    url:        'main.html',
    type:       'GET',
    dataType:   'text', 

    success: function( response ) {
      // show page
      $('#sigbro_spa').html( response );

      // autofill
      var accAUTO   = localStorage.getItem("sigbro_wallet_autologin");
      $('#sigbro_index-input-account').val(accAUTO);
    },

    error: function ( error ) {
      console.log('ERROR: ', error);
    },

    complete: function( xhr, status ) {

      // index // LOG IN CLICK
      $(document).on('click', '#sigbro_index-button-login', function(e) {
        e.preventDefault();
        var accRS = $('#sigbro_index-input-account').val();
        console.log(accRS);
        // ARDOR-ZZZZ-48G3-9F9W-4CLJZ
        var ardorRegex = /^ARDOR-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{5}/ig
        var nxtRegex = /^NXT-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{5}/ig

        if ( ardorRegex.test ( accRS ) || nxtRegex.test( accRS ) ) {
          localStorage.setItem("sigbro_wallet_accountRS", accRS);
          getPublicKey_v2(accRS, 'ardor');
          getPublicKey_v2(accRS, 'nxt');
          if ( document.getElementById('sigbro_index-rememberme').checked ) { 
            // save account 
            localStorage.setItem("sigbro_wallet_autologin", accRS);
          } 

          localStorage.setItem("sigbro_wallet_page", "profile");
          show_profile(); 
        } else {
          alert("Check your accountRS and try again.");
        }
      });
    }
  });

}

function show_auth() {
  $.ajax({ 
    url:        'auth.html',
    type:       'GET',
    dataType:   'text', 

    success: function( response ) {
      // show page
      $('#sigbro_spa').html( response );
    },
    error: function ( error ) {
      console.log('ERROR: ', error);
    },
    complete: function( xhr, status ) {
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
  if ( accRS == null ) { sigbro_clear_localstorage(); location.href = "/index.html"; }
  document.getElementById('sigbro_send_senderRS').value = accRS; 
  document.getElementById('sigbro_template_recipientRS').value = accRS; 

  var senderPubKey= localStorage.getItem("sigbro_pubkey_" + accRS );
  if ( senderPubKey == null ) {
    getPublicKey_v2(accRS, 'ardor');
    getPublicKey_v2(accRS, 'nxt');
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
$(document).on('click', '#sigbro_template_submit', function(e) {
  var msg_block = document.getElementById('sigbro_template_messages_block');
  msg_block.setAttribute('style', 'display:none;');

	var recipientRS   = document.getElementById('sigbro_template_recipientRS').value;
  var amount        = document.getElementById('sigbro_template_amount').value;
  var currencie     = document.getElementById('sigbro_template_currencie').value;
  var operation     = document.getElementById('sigbro_template_operation').value;

  /*
  var encrypt_msg = 0;
  if ( document.getElementById('sigbro_template_encrypt_message').checked ) {
    encrypt_msg = 1;
  }
  */
  
  var msg         = document.getElementById('sigbro_template_message').value;


  var url = TEMPLATEURL + "/api/v1/add/";

  template = {  
                  "network" : NETWORK,
                  "chain" : currencie, 
                  "requestType" : operation,
                  "recipientRS" : recipientRS, 
                  "amount" : amount, 
                  "message" : msg
                }; 

  param = JSON.stringify(
    { "template" : template }
  );

  console.log( "url: " + url); 
  console.log( "params: " + param );

  sendJSON( url, param, TIMEOUT, page_ops_template_show_result );
});

// template operator response
function page_ops_template_show_result() {
  var resp = this.responseText;
  var resp_j = JSON.parse(resp);
    
  console.log("RESULT:");
  console.log(resp_j);

  if ( resp_j.error  ) { 
    page_ops_show_alert( resp_j.error );
  } else if ( resp_j.uuid ) { 
    var resp_url = "https://sigbro-template.api.nxter.org/api/v1/get/" + resp_j.uuid + "/";
    console.log( "URL: " + resp_url );
    localStorage.setItem("sigbro_wallet_url", resp_url);
    show_qr();
  }
}



$(document).on('click', '#sigbro_send_submit', function(e) {
  var msg_block = document.getElementById('sigbro_send_messages_block');
  msg_block.setAttribute('style', 'display:none;');

	var senderRS    = document.getElementById('sigbro_send_senderRS').value;

  var senderPubKey= localStorage.getItem("sigbro_pubkey_" + senderRS );

  if ( senderPubKey == null ) {
    page_ops_show_alert ("Your account does not have PublicKey. You can not send any transaction with SIGBRO WALLET, sorry");
    return;
  }
  
  var recipientRS = document.getElementById('sigbro_send_recipientRS').value; 
  var amount      = document.getElementById('sigbro_send_amount').value;
  var fee = -1;

  var encrypt_msg = 0;
  // check encrypt or plain text for msg
  if ( document.getElementById('sigbro_encrypt_message').checked ) {
    encrypt_msg = 1;
  }
  
  var currencie   = document.querySelector('input[name = "sigbro_send_selector"]:checked').value;
  var msg         = document.getElementById('sigbro_send_message').value;


  var url = APIURL + "/api/v2/sendmoney/";

  param_json = { "currencie" : currencie, "recipient" : recipientRS, "amount" : amount, "publicKey" : senderPubKey, "fee" : fee, "msg" : msg, "encrypt_msg" : encrypt_msg }; 
  param = JSON.stringify(param_json);

  console.log( "url: " + url);
  console.log( "params: " + param );

  sendJSON( url, param, TIMEOUT, page_ops_show_result );
});


function page_ops_show_result() {
  var resp = this.responseText;
  var resp_j = JSON.parse(resp);
    
  console.log("RESULT:");
  console.log(resp_j);

  if ( resp_j.error  ) { 
    page_ops_show_alert( resp_j.error );
    //alert ( resp_j.error ); 
  } else if ( resp_j.url ) { 
    console.log( "URL: " + resp_j.url );
    localStorage.setItem("sigbro_wallet_url", resp_j.url);
    show_qr();
  }
}

/////////////////////////////////// QR
function page_qr_show_qrcode() {
  var accURL = localStorage.getItem("sigbro_wallet_url");

  if ( accURL == null ) { 
    //document.getElementById('sigbro_qr-code').textContent = "You does not have any relevant data for QR code"; 
    return; 
  }

  var link = document.getElementById("sigbro_qr-url");
  //link.textContent = accURL;
  link.textContent = "Open Tx in Browser";
  link.setAttribute("href", accURL);

  var sigbroURL = accURL.replace("https", "sigbro");
  var link_sigbro = document.getElementById("sigbro_qr--mobile_url");
  link_sigbro.setAttribute("href", sigbroURL );

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
    var sigbroUUID= JSON.parse( localStorage.getItem("sigbro_uuid") );
  } catch (err) {
    return;
  }
  if ( sigbroUUID == null ) { 
    return; 
  }

  var uuid = sigbroUUID.uuid;
  var url = "sigbro://"+uuid;
  console.log(url);

  var QRC = qrcodegen.QrCode;
  var qr0 = QRC.encodeText(url, QRC.Ecc.HIGH);
  var code = qr0.toSvgString(4);
  
  var svg = document.getElementById("sigbro_auth--qr_code_sigbromobile");
  svg.setAttribute("viewBox", / viewBox="([^"]*)"/.exec(code)[1]);
  svg.querySelector("path").setAttribute("d", / d="([^"]*)"/.exec(code)[1]);
  svg.style.removeProperty("display");
}



/////////////////////////////////// PORTFOLIO

// save assets info
function page_portfolio_save_assets() {
  var resp = this.responseText;
  var respJSON = JSON.parse(resp);
  // console.log(respJSON);

  if ( respJSON.data ) {
    var timestamp = Date.now() ; 
    var tmp = { 'value': respJSON.data ,   'timestamp': timestamp };
    localStorage.setItem('sigbro_wallet_assets', JSON.stringify(tmp));

    page_portfolio_show_assets();
  } else {
    console.log(respJSON);
  }

}

//show assets
function page_portfolio_show_assets() {
  var accRS   = localStorage.getItem("sigbro_wallet_accountRS");
  var assets  = localStorage.getItem("sigbro_wallet_assets");

  if ( assets == null ) {
    var url = APIURL + "/api/v2/assets/" + accRS + "/en/";
    getJSON(url, 3000, page_portfolio_save_assets, "assets");
    return;
  }

  assets_data         = JSON.parse(assets);

  // If delta > 5 min need to get new balances
  var delta = Date.now() - assets_data.timestamp;
  console.log("Delta: " + delta/1000 + " sec.");
  if ( delta > 5*60*1000 ) {
    var url = APIURL + "/api/v2/assets/" + accRS + "/en/";
    getJSON(url, 3000, page_portfolio_save_assets, "assets");
    return;
  }

  document.getElementById('sigbro_wallet_assets').innerHTML = assets_data.value; 
}

// save currencies
function page_portfolio_save_currencies() {
  var resp = this.responseText;
  var respJSON = JSON.parse(resp);
  // console.log(respJSON);

  if ( respJSON.data ) {
    var timestamp = Date.now() ; 
    var tmp = { 'value': respJSON.data ,   'timestamp': timestamp };
    localStorage.setItem('sigbro_wallet_currencies', JSON.stringify(tmp));

    page_portfolio_show_currencies();
  } else {
    console.log(respJSON);
  }

}

function page_portfolio_show_currencies() {
  var accRS       = localStorage.getItem("sigbro_wallet_accountRS");
  var currencies  = localStorage.getItem("sigbro_wallet_currencies");

  if ( currencies == null ) {
    var url = APIURL + "/api/v2/currencies/" + accRS + "/en/";
    getJSON(url, 3000, page_portfolio_save_currencies, "currencies");
    return;
  }

  curr_data = JSON.parse(currencies);

  // If delta > 5 min need to get new balances
  var delta = Date.now() - curr_data.timestamp;
  console.log("Delta: " + delta/1000 + " sec.");
  if ( delta > 5*60*1000 ) {
    var url = APIURL + "/api/v2/currencies/" + accRS + "/en/";
    getJSON(url, 3000, page_portfolio_save_currencies, "currencies");
    return;
  }

  document.getElementById('sigbro_wallet_currencies').innerHTML = curr_data.value; 
}


/////////////////////////////////// PROFILE

function page_profile_set_accountRS() {
  var accRS = localStorage.getItem("sigbro_wallet_accountRS");
  if ( accRS == null ) { sigbro_clear_localstorage(); location.href = "/index.html"; }

  document.getElementById('sigbro_profile-accountRS').textContent = accRS; 
}

// callback function for userinf
function page_profile_save_userinfo(data) {
  var resp = this.responseText;

  var respJSON = JSON.parse(resp);

  if ( respJSON.name ) {
    localStorage.setItem('sigbro_wallet_username', respJSON.name );
  } else {
    localStorage.setItem('sigbro_wallet_username', 'NoName' );
  }

  if ( respJSON.description ) {
    localStorage.setItem('sigbro_wallet_userdesc', respJSON.description );
  } else {
    localStorage.setItem('sigbro_wallet_userdesc', '' );
  }

  page_profile_set_userinfo();
}

function page_profile_set_userinfo() {
  // get username from localstorage
  var accRS   = localStorage.getItem("sigbro_wallet_accountRS");
  var accName = localStorage.getItem('sigbro_wallet_username');
  var accDesc = localStorage.getItem('sigbro_wallet_userdesc');

  if ( accName == null || accDesc == null ) {
    // need to get info from blockchain
    var url = ARDOR + "?requestType=getAccount&account=" + accRS;
    getJSON(url, 3000, page_profile_save_userinfo, "custom text");
    return;
  } 

  document.getElementById('sigbro_profile-username').textContent = accName; 
  document.getElementById('sigbro_profile-userdesc').textContent = accDesc; 

}

// callback function for NXT balance
function page_profile_set_balance_nxt(data) {
  var resp = this.responseText;
  var respJSON = JSON.parse(resp);
  if ( respJSON.balanceNQT ) {
    var nxt = respJSON.balanceNQT / Math.pow(10,8);
    var tmp = { 'value': nxt, 'timestamp': Date.now() };
    localStorage.setItem('sigbro_wallet_balance_nxt', JSON.stringify(tmp));
    page_profile_show_balance_nxt()
  } else {
    // problem while getting balance
    document.getElementById('sigbro_profile-balance-nxt').textContent = 'NaN';
    console.log(respJSON);
  }

}

// show nxt balance on the page
function page_profile_show_balance_nxt() {
  var accRS   = localStorage.getItem("sigbro_wallet_accountRS");
  var accBalanceNxt = localStorage.getItem('sigbro_wallet_balance_nxt');

  if ( accBalanceNxt == null ) {
    var url = NXT + "?requestType=getAccount&account=" + accRS;
    getJSON(url, 3000, page_profile_set_balance_nxt, "balance NXT");
    return;
  }

  // If delta > 5 min need to get new balances
  var delta = Date.now() - accBalanceNxt.timestamp;
  if ( delta > 5*60*1000 ) {
    var url = NXT + "?requestType=getAccount&account=" + accRS;
    getJSON(url, 3000, page_profile_set_balance_nxt, "balance NXT");
    return;
  }

  accBalanceNxt = JSON.parse(accBalanceNxt);
  document.getElementById('sigbro_profile-balance-nxt').textContent = accBalanceNxt.value; 
}

// callback function for ARDOR balance
function page_profile_set_balance_ardor(data) {
  var resp = this.responseText;
  var respJSON = JSON.parse(resp);
  console.log(respJSON);

  if ( respJSON.balances ) {
    // get correct response
    var timestamp = Date.now() ; 
    var ardor     = respJSON.balances[1].balanceNQT / Math.pow(10,8);
    var ignis     = respJSON.balances[2].balanceNQT / Math.pow(10,8);
    var aeur      = respJSON.balances[3].balanceNQT / Math.pow(10,4);
    var bitswift  = respJSON.balances[4].balanceNQT / Math.pow(10,8);

    var tmp = { 'value': ardor,   'timestamp': timestamp };
    localStorage.setItem('sigbro_wallet_balance_ardor', JSON.stringify(tmp));

    var tmp = { 'value': ignis,   'timestamp': timestamp };
    localStorage.setItem('sigbro_wallet_balance_ignis', JSON.stringify(tmp));

    var tmp = { 'value': aeur,    'timestamp': timestamp };
    localStorage.setItem('sigbro_wallet_balance_aeur', JSON.stringify(tmp));

    var tmp = { 'value': bitswift,'timestamp': timestamp };
    localStorage.setItem('sigbro_wallet_balance_bitswift', JSON.stringify(tmp));

    page_profile_show_balance_ardor()
  } else {
    document.getElementById('sigbro_profile-balance-ardor').textContent     = "NaN"; 
    document.getElementById('sigbro_profile-balance-ignis').textContent     = "NaN";
    document.getElementById('sigbro_profile-balance-aeur').textContent      = "NaN";
    document.getElementById('sigbro_profile-balance-bitswift').textContent  = "NaN";
    console.log(respJSON);
  }

}

// set ardor, ignis, aeur, bitswift balance on the page
function page_profile_show_balance_ardor() {
  var accRS   = localStorage.getItem("sigbro_wallet_accountRS");
  var accBalanceArdor     = localStorage.getItem('sigbro_wallet_balance_ardor');
  var accBalanceIgnis     = localStorage.getItem('sigbro_wallet_balance_ignis');
  var accBalanceAeur      = localStorage.getItem('sigbro_wallet_balance_aeur');
  var accBalanceBitswift  = localStorage.getItem('sigbro_wallet_balance_bitswift');

  if ( accBalanceArdor == null || accBalanceIgnis == null || accBalanceAeur == null || accBalanceBitswift == null ) {
    var url = ARDOR + "?requestType=getBalances&account=" + accRS + "&chain=1&chain=2&chain=3&chain=4";
    getJSON(url, 3000, page_profile_set_balance_ardor, "balance ARDOR");
    return;
  }

  accBalanceArdor     = JSON.parse(accBalanceArdor);
  accBalanceIgnis     = JSON.parse(accBalanceIgnis);
  accBalanceAeur      = JSON.parse(accBalanceAeur);
  accBalanceBitswift  = JSON.parse(accBalanceBitswift);

  
  // If delta > 5 min need to get new balances
  var delta = Date.now() - accBalanceArdor.timestamp;
  console.log("Delta: " + delta/1000 + " sec.");
  if ( delta > 5*60*1000 ) {
    var url = ARDOR + "?requestType=getBalances&account=" + accRS + "&chain=1&chain=2&chain=3&chain=4";
    getJSON(url, 3000, page_profile_set_balance_ardor, "balance ARDOR");
    return;
  }

  document.getElementById('sigbro_profile-balance-ardor').textContent = accBalanceArdor.value; 
  document.getElementById('sigbro_profile-balance-ignis').textContent = accBalanceIgnis.value; 
  document.getElementById('sigbro_profile-balance-aeur').textContent = accBalanceAeur.value; 
  document.getElementById('sigbro_profile-balance-bitswift').textContent = accBalanceBitswift.value; 

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

  localStorage.removeItem("sigbro_wallet_balance_nxt");
  localStorage.removeItem("sigbro_wallet_balance_aeur");
  localStorage.removeItem("sigbro_wallet_balance_ardor");
  localStorage.removeItem("sigbro_wallet_balance_ignis");
  localStorage.removeItem("sigbro_wallet_balance_bitswift");

  localStorage.removeItem("sigbro_wallet_url"); // last created url
  localStorage.removeItem("sigbro_uuid"); // uuid from last logon
}

function sigbro_clear_balances() {
  localStorage.removeItem("sigbro_wallet_assets");
  localStorage.removeItem("sigbro_wallet_currencies");

  localStorage.removeItem("sigbro_wallet_balance_nxt");
  localStorage.removeItem("sigbro_wallet_balance_aeur");
  localStorage.removeItem("sigbro_wallet_balance_ardor");
  localStorage.removeItem("sigbro_wallet_balance_ignis");
  localStorage.removeItem("sigbro_wallet_balance_bitswift");

  localStorage.removeItem("sigbro_wallet_url"); // last created url
  localStorage.removeItem("sigbro_uuid"); // uuid from last logon
}

$(document).on('click', '#sigbro-logout', function(e) {
  e.preventDefault();
  localStorage.setItem("sigbro_wallet_page", "index");
  sigbro_clear_localstorage();
  show_index();
});

$(document).on('click', '#sigbro-change-network', function(e) {
  e.preventDefault();

  var network = localStorage.getItem("sigbro_wallet_network");
  if ( network == null ) {
    localStorage.setItem("sigbro_wallet_network", "testnet");
    network = "testnet";
  }
  if ( network == 'mainnet' ) { 
    localStorage.setItem("sigbro_wallet_network", "testnet");
  } else {
    localStorage.setItem("sigbro_wallet_network", "mainnet");
  }

  sigbro_clear_balances();
  location.reload();
});

// change auth type: accountRS or SIGBRO MOBILE
$(document).on('click', '#sigbo_index--btn_auth_accountrs', function(e) {
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

$(document).on('click', '#sigbo_index--btn_auth_sigbro', function(e) {
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
    
  console.log(resp_j);
}

// click on OPEN SIGBRO MOBILE
$(document).on('click', '#sigbo_index--btn_open_sigbro_mobile', function(e) {
  e.preventDefault();

  var timestamp = Date.now() ; 
  var old_timestamp = 0;
  var old_uuid = "";
  var uuid = "";
  
  //TODO: Get uuid from localstorage and check time, if more than 15 min update uuid
  try {
    var uuid_from_localstorage = JSON.parse( localStorage.getItem("sigbro_uuid") );
    old_timestamp = uuid_from_localstorage.timestamp;
    old_uuid = uuid_from_localstorage.uuid;
  } catch (err) {
    console.log("Incorrect json in localstorage");
  }

  console.log("Delta: " + (timestamp-old_timestamp) );

  if ( timestamp - old_timestamp < 15*60*1000 ) {
    uuid = old_uuid;
    console.log("Using old UUID: " + uuid);
  } else {
    uuid = uuidv4();
    console.log("Using new UUID: " + uuid);

    var uuid_timestamp = { "uuid" : uuid, "timestamp" : timestamp }
    localStorage.setItem("sigbro_uuid", JSON.stringify(uuid_timestamp) );

    // if uuid is new, send it to our API
    url = "https://random.nxter.org/api/auth/new";

    param_json = { "uuid" : uuid }; 
    param = JSON.stringify(param_json);

    sendJSON( url, param, 3000, add_new_uuid_result );
  }

  var source = new EventSource('https://random.nxter.org:9040/stream');

  // subscribe to global events from auth-sse
  source.addEventListener('greeting', function(event) {
    console.log('Gloabal event');
    var data = JSON.parse(event.data);
    console.log(data);
    console.log(event);
  }, false);

  // subscribe to personal events from auth-sse
  source.addEventListener( uuid, function(event) {
    var data = JSON.parse(event.data);

    try { 
      var data2 = JSON.parse(data);
    } catch (err) {
      var data2 = data;
    }

    console.log(data2);

    if ( data2.type == 'success' && data2.accountRS ) {
      localStorage.setItem("sigbro_wallet_accountRS", data2.accountRS);
      getPublicKey_v2(data2.accountRS, 'ardor');
      getPublicKey_v2(data2.accountRS, 'nxt');
      localStorage.setItem("sigbro_wallet_page", "profile");
      localStorage.removeItem("sigbro_uuid");
      show_profile(); 
    } else {
      localStorage.removeItem("sigbro_uuid");
      alert( data2.message );
    }
  }, false);


  // need to open sigbro://UUIDv4 url
  var url_sigbro = "sigbro://" + uuid;
  window.open(url_sigbro, '_blank');

});


// click on show qr code
$(document).on('click', '#sigbo_index--btn_scan_qr_code', function(e) {
  e.preventDefault();

  var timestamp = Date.now() ; 
  var old_timestamp = 0;
  var old_uuid = "";
  var uuid = "";
  
  //TODO: Get uuid from localstorage and check time, if more than 15 min update uuid
  try {
    var uuid_from_localstorage = JSON.parse( localStorage.getItem("sigbro_uuid") );
    old_timestamp = uuid_from_localstorage.timestamp;
    old_uuid = uuid_from_localstorage.uuid;
  } catch (err) {
    console.log("Incorrect json in localstorage");
  }

  console.log("Delta: " + (timestamp-old_timestamp) );

  if ( timestamp - old_timestamp < 15*60*1000 ) {
    uuid = old_uuid;
    console.log("Using old UUID: " + uuid);
  } else {
    uuid = uuidv4();
    console.log("Using new UUID: " + uuid);

    var uuid_timestamp = { "uuid" : uuid, "timestamp" : timestamp }
    localStorage.setItem("sigbro_uuid", JSON.stringify(uuid_timestamp) );

    // if uuid is new, send it to our API
    url = "https://random.nxter.org/api/auth/new";

    param_json = { "uuid" : uuid }; 
    param = JSON.stringify(param_json);

    sendJSON( url, param, 3000, add_new_uuid_result );
  }

  show_auth();
  var source = new EventSource('https://random.nxter.org:9040/stream');

  // subscribe to global events from auth-sse
  source.addEventListener('greeting', function(event) {
    console.log('Gloabal event');
    var data = JSON.parse(event.data);
    console.log(data);
    console.log(event);
  }, false);

  // subscribe to personal events from auth-sse
  source.addEventListener( uuid, function(event) {
    var data = JSON.parse(event.data);

    try { 
      var data2 = JSON.parse(data);
    } catch (err) {
      var data2 = data;
    }

    console.log(data2);

    if ( data2.type == 'success' && data2.accountRS ) {
      localStorage.setItem("sigbro_wallet_accountRS", data2.accountRS);
      getPublicKey_v2(data2.accountRS, 'ardor');
      getPublicKey_v2(data2.accountRS, 'nxt');
      localStorage.setItem("sigbro_wallet_page", "profile");
      localStorage.removeItem("sigbro_uuid");
      show_profile(); 
    } else {
      localStorage.removeItem("sigbro_uuid");
      alert( data2.message );
    }
  }, false);


});




// end change auth type: accountRS or SIGBRO MOBILE

function getJSON(url, timeout, callback) {
	var args = Array.prototype.slice.call(arguments, 3);
	var xhr = new XMLHttpRequest();
	xhr.ontimeout = function () {
		console.log("The request for " + url + " timed out.");
	};
	xhr.onload = function() {
		if (xhr.readyState === 4) {
			if (xhr.status === 200) {
        console.log('get: ' + url + ' success.');
				callback.apply(xhr, args);
			} else {
				console.log(xhr.statusText);
			}
		}
	};
	xhr.open("GET", url, true);
	xhr.timeout = timeout;
	xhr.send(null);
}

function sendJSON(url, params, timeout, callback) {
	var args = Array.prototype.slice.call(arguments, 3);
  var xhr = new XMLHttpRequest();
	xhr.ontimeout = function () {
		console.log("The POST request for " + url + " timed out.");
	};
	xhr.onload = function() {
		if (xhr.readyState === 4) {
			if (xhr.status === 200) {
        console.log('post: ' + url + ' success.');
				callback.apply(xhr, args);
			} else {
				console.log(xhr.statusText);
			}
		}
	};
  xhr.open("POST", url);
  xhr.setRequestHeader('Content-type', 'application/json');
	xhr.timeout = timeout;
  xhr.send(params);
}

function getPublicKey(accountRS, network) {
  var pubKey = localStorage.getItem("sigbro_pubkey_"+accountRS);
  if ( pubKey == null ) {
    var url = network + "?requestType=getAccountPublicKey&account="+accountRS;
    getJSON(url, 3000, savePublicKey, accountRS);
  }
}

function getPublicKey_v2(accountRS, network) {
  // network = ardor / nxt
  // prefix from localstorage
  var pubKey = localStorage.getItem("sigbro_pubkey_"+accountRS);
  if ( pubKey == null ) {
    var _network  = localStorage.getItem("sigbro_wallet_network");
    if ( _network == 'mainnet' ) {
      _prefix = '';
    } else {
      _prefix = 'tst';
    }

    var url = "https://random.nxter.org/" + _prefix + network + "?requestType=getAccountPublicKey&account=" + accountRS;
    getJSON(url, 3000, savePublicKey, accountRS);
  }
}

function savePublicKey(accountRS) {
  // accountRS getting from getJSON additional param (last)
  var resp = this.responseText;
  resp = JSON.parse(resp);

  if ( resp.publicKey ) {
    console.log('Saving public key.');
    localStorage.setItem("sigbro_pubkey_"+accountRS, resp.publicKey);
  }
}


// https://stackoverflow.com/questions/105034/create-guid-uuid-in-javascript
function uuidv4() { // Public Domain/MIT
  var d = new Date().getTime();
  if (typeof performance !== 'undefined' && typeof performance.now === 'function'){
      d += performance.now(); //use high-precision timer if available
  }
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
      var r = (d + Math.random() * 16) % 16 | 0;
      d = Math.floor(d / 16);
      return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
  });
}

function page_show_network_type() {
  // check localstorage for network type and update button
  var network = localStorage.getItem("sigbro_wallet_network");
  console.log('Network: ' + network)
  if ( network == null ) {
    localStorage.setItem("sigbro_wallet_network", "testnet");
  }
  if ( network == 'mainnet' ) { 
    network = 'mainnet';
  } else {
    network = 'testnet';
  }
  document.getElementById('sigbro-change-network').innerHTML = network; 
}


