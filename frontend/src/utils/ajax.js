
import { IsStr, IsArr } from './index'
import { Warn, Danger } from './alert'
import $ from 'jquery';

function checkSession(error) {
  if (IsStr(error) && error === "session.expired") {
    Warn("请登录后再进行操作");
  }
}

export function GetJSON(url, params, on_success, on_error) {
  $.getJSON('/api' + url, params, on_success)
    .fail(function (jqXHR, textStatus, errorThrown) {

      if (jqXHR) {
        console.log(jqXHR.statusText);
        const error = jqXHR.responseText;
        const _errorMessadge = JSON.parse(error)
        checkSession(error);
        _errorMessadge && Danger(_errorMessadge.ApiError.message);
        on_error && on_error(error);
      }

    })
}

export function Get(url, params, on_success, on_error) {
  $.get('/api' + url, params, on_success)
    .fail(function (jqXHR, textStatus, errorThrown) {

      if (jqXHR) {
        console.log(jqXHR.statusText);
        const error = jqXHR.responseText;
        const _errorMessadge = JSON.parse(error)
        checkSession(error);
        _errorMessadge && Danger(_errorMessadge.ApiError.message);
        on_error && on_error(error);
      }

    })
}

export function PostJSON(url, { params, data, type }, on_success, on_error) {
  var url_params = '';
  for (const key in params) {
    url_params += url_params ? '&' : '?';
    const val = params[key];
    if (IsArr(val)){
      for (var i = 0; i < val.length; i++) {
        const _val = val[i];
        url_params += key + '=' + _val;
      }
    }
    else
      url_params += key + '=' + params[key];
  }
  $.ajax({
    url: '/api' + url + url_params,
    type: type ? type : "POST",
    contentType: "application/json; charset=utf-8",
    data: JSON.stringify(data), //Stringified Json Object
    async: true, //Cross-domain requests and dataType: "jsonp" requests do not support synchronous operation
    cache: false, //This will force requested pages not to be cached by the browser          
    processData: false, //To avoid making query String instead of JSON
    success: on_success
  }).fail(function (jqXHR, textStatus, errorThrown) {
    if (jqXHR) {
      console.log(jqXHR.statusText);
      const error = jqXHR.responseText;
      const _errorMessadge = JSON.parse(error)
      checkSession(error);
      _errorMessadge && Danger(_errorMessadge.ApiError.message);
      on_error && on_error(error);
    }
  })
}


export function Post(url, params, on_success, on_error) {
  $.post('/api' + url, params, on_success)
    .fail(function (jqXHR, textStatus, errorThrown) {
      if (jqXHR) {
        console.log(errorThrown);
        const error = jqXHR.responseText;
        checkSession(error);
        on_error && on_error(error);
      }
    }
    )
}

