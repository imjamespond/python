import $ from 'jquery';

$.ajaxSetup({
  cache: false
});

export const StopPropagation = function (e) {
  e = e || window.event;
  if (e.stopPropagation) {
    e.stopPropagation();
  } else {
    e.cancelBubble = true;
  }
}
export const PreventDefault = function (e) {
  e.preventDefault();
}

// const SHA1 = require('./sha1');
// console.log(process.env.CONTEXT_PATH);
export const ContextPath = process.env.CONTEXT_PATH;

export const GetImgUrl = function (url) {
  if (process.env.NODE_ENV === 'development')
    return `/dist/images/${url}`;
  return `${process.env.CONTEXT_PATH}/dist/images/${url}`;
}

export const IsObj = function (data) {
  return data && (typeof data) === "object"
}

export const IsArr = function (data) {
  return data && Object.prototype.toString.call(data) === '[object Array]';
}

export const IsStr = function (data) {
  return data && (typeof data) === "string"
}

export const GetLocaleDate = function (time) {
  var d = new Date();
  d.setTime(time);
  return d.toLocaleDateString('zh-CN')
}

export const GetUrlParts = function (url) {
  var a = document.createElement('a');
  a.href = url;
  return {
    href: a.href,
    host: a.host,
    hostname: a.hostname,
    port: a.port,
    pathname: a.pathname,
    protocol: a.protocol,
    hash: a.hash,
    search: a.search
  };
}

export const Open = function (url, params) {
  params = params || {};
  return window.open(url, params.target || '_blank');//_self
}

export const Redirect = function (redirect) {
  // location.hash = '#'+redirect; 
  window.location.href = process.env.CONTEXT_PATH + redirect;
}

export const SimpleDate = function (date) {
  return new Date(date).toLocaleDateString('zh-CN');
}

// export const GetDateString = function (now) {
//   Date.prototype.format = function (format) {
//     var date = {
//       "M+": this.getMonth() + 1,
//       "d+": this.getDate(),
//       "h+": this.getHours(),
//       "m+": this.getMinutes(),
//       "s+": this.getSeconds(),
//       "q+": Math.floor((this.getMonth() + 3) / 3),
//       "S+": this.getMilliseconds()
//     };
//     if (/(y+)/i.test(format)) {
//       format = format.replace(RegExp.$1, (this.getFullYear() + '').substr(4 - RegExp.$1.length));
//     }
//     for (var k in date) {
//       if (new RegExp("(" + k + ")").test(format)) {
//         format = format.replace(RegExp.$1, RegExp.$1.length === 1 ? date[k] : ("00" + date[k]).substr(("" + date[k]).length));
//       }
//     }
//     return format;
//   };
//   var date = new Date(now);
//   return date.format('yyyy-MM-dd');
// }


// export const GetSha1 = function (str) {
//   if (null == str)
//     str = ""
//   var sha1 = new SHA1("SHA-1", "TEXT")
//   sha1.update(str)
//   return sha1.getHash("HEX")
// }

export const UpdateFormData = function (formData, obj) {
  for (var key in formData)
    formData && obj && key in obj && (formData[key] = obj[key]);
  // console.log(formData)
}

/*
// Usage:
// query string: ?foo=lorem&bar=&baz
var foo = GetParameterByName('foo'); // "lorem"
var bar = GetParameterByName('bar'); // "" (present with empty value)
var baz = GetParameterByName('baz'); // "" (present with no value)
var qux = GetParameterByName('qux'); // null (absent)
*/
export const GetParameterByName = function (name, url) {
  url = url || window.location.href;
  name = name.replace(/[\[\]]/g, "\\$&");
  var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
    results = regex.exec(url);
  if (!results) return null;
  if (!results[2]) return '';
  return decodeURIComponent(results[2].replace(/\+/g, " "));
}

export const XOR = function (a, b) {
  return (a ? 1 : 0) ^ (b ? 1 : 0);
}
