(function(){function r(e,n,t){function o(i,f){if(!n[i]){if(!e[i]){var c="function"==typeof require&&require;if(!f&&c)return c(i,!0);if(u)return u(i,!0);var a=new Error("Cannot find module '"+i+"'");throw a.code="MODULE_NOT_FOUND",a}var p=n[i]={exports:{}};e[i][0].call(p.exports,function(r){var n=e[i][1][r];return o(n||r)},p,p.exports,r,e,n,t)}return n[i].exports}for(var u="function"==typeof require&&require,i=0;i<t.length;i++)o(t[i]);return o}return r})()({1:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: !0
});

var e = function() {
  function e() {
    this.DEBUG = 1, this.INFO = 2, this.WARNING = 3, this.ERROR = 4, this.$level = this.INFO;
  }
  return Object.defineProperty(e.prototype, "level", {
    get: function() {
      return this.$level;
    },
    enumerable: !1,
    configurable: !0
  }), e.prototype.setLevel = function(e) {
    this.$level = e, this.d("Set log level: " + e);
  }, e.prototype.d = function(e, r) {
    this.$level <= this.DEBUG && send({
      $log: {
        level: "debug",
        message: e
      }
    }, r);
  }, e.prototype.i = function(e, r) {
    this.$level <= this.INFO && send({
      $log: {
        level: "info",
        message: e
      }
    }, r);
  }, e.prototype.w = function(e, r) {
    this.$level <= this.WARNING && send({
      $log: {
        level: "warning",
        message: e
      }
    }, r);
  }, e.prototype.e = function(e, r) {
    this.$level <= this.ERROR && send({
      $log: {
        level: "error",
        message: e
      }
    }, r);
  }, e;
}(), r = function() {
  function e() {}
  return e.prototype.load = function(e, r) {
    Object.defineProperties(globalThis, {
      parameters: {
        configurable: !0,
        enumerable: !0,
        value: r
      }
    });
    for (var t = 0, n = e; t < n.length; t++) {
      var o = n[t];
      try {
        (0, eval)(o.source);
      } catch (e) {
        var l = e.hasOwnProperty("stack") ? e.stack : e;
        throw new Error("Unable to load ".concat(o.filename, ": ").concat(l));
      }
    }
  }, e;
}(), t = new r;

rpc.exports = {
  loadScripts: t.load.bind(t)
};

var n = require("./lib/c"), o = require("./lib/java"), l = require("./lib/android"), i = require("./lib/objc"), a = require("./lib/ios"), u = new e, s = new n.CHelper, c = new o.JavaHelper, p = new l.AndroidHelper, v = new i.ObjCHelper, f = new a.IOSHelper;

Object.defineProperties(globalThis, {
  Log: {
    enumerable: !0,
    value: u
  },
  CHelper: {
    enumerable: !0,
    value: s
  },
  JavaHelper: {
    enumerable: !0,
    value: c
  },
  AndroidHelper: {
    enumerable: !0,
    value: p
  },
  ObjCHelper: {
    enumerable: !0,
    value: v
  },
  IOSHelper: {
    enumerable: !0,
    value: f
  },
  ignoreError: {
    enumerable: !1,
    value: function(e, r) {
      void 0 === r && (r = void 0);
      try {
        return e();
      } catch (e) {
        return u.d("Catch ignored error. " + e), r;
      }
    }
  },
  parseBoolean: {
    enumerable: !1,
    value: function(e, r) {
      if (void 0 === r && (r = void 0), "boolean" == typeof e) return e;
      if ("string" == typeof e) {
        var t = e.toLowerCase();
        if ("true" === t) return !0;
        if ("false" === t) return !1;
      }
      return r;
    }
  },
  pretty2String: {
    enumerable: !1,
    value: function(e) {
      return (e = pretty2Json(e)) instanceof Object ? JSON.stringify(e) : e;
    }
  },
  pretty2Json: {
    enumerable: !1,
    value: function(e) {
      if (!(e instanceof Object)) return e;
      if (Array.isArray(e) || c.isArray(e)) {
        for (var r = [], t = 0; t < e.length; t++) r.push(pretty2Json(e[t]));
        return r;
      }
      return ignoreError((function() {
        return e.toString();
      }));
    }
  }
});

},{"./lib/android":2,"./lib/c":3,"./lib/ios":4,"./lib/java":5,"./lib/objc":6}],2:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: !0
}), exports.AndroidHelper = void 0;

var e = function() {
  function e() {}
  return e.prototype.setWebviewDebuggingEnabled = function() {
    Log.w("Android Enable Webview Debugging"), Java.perform((function() {
      var e = "android.webkit.WebView";
      JavaHelper.hookMethods(e, "setWebContentsDebuggingEnabled", (function(e, r) {
        return Log.d("android.webkit.WebView.setWebContentsDebuggingEnabled: " + r[0]), 
        r[0] = !0, this(e, r);
      })), JavaHelper.hookMethods(e, "loadUrl", (function(e, r) {
        return Log.d("android.webkit.WebView.loadUrl: " + r[0]), e.setWebContentsDebuggingEnabled(!0), 
        this(e, r);
      }));
      ignoreError((function() {
        return JavaHelper.hookMethods(e, "setWebContentsDebuggingEnabled", (function(e, r) {
          return Log.d("com.uc.webview.export.WebView.setWebContentsDebuggingEnabled: " + r[0]), 
          r[0] = !0, this(e, r);
        }));
      })), ignoreError((function() {
        return JavaHelper.hookMethods("com.uc.webview.export.WebView", "loadUrl", (function(e, r) {
          return Log.d("com.uc.webview.export.WebView.loadUrl: " + r[0]), e.setWebContentsDebuggingEnabled(!0), 
          this(e, r);
        }));
      }));
    }));
  }, e.prototype.bypassSslPinning = function() {
    Log.w("Android Bypass ssl pinning"), Java.perform((function() {
      var e = Java.use("java.util.Arrays");
      ignoreError((function() {
        return JavaHelper.hookMethods("com.android.org.conscrypt.TrustManagerImpl", "checkServerTrusted", (function(r, o) {
          if (Log.d("Bypassing TrustManagerImpl checkServerTrusted"), "void" != this.returnType.type) return "pointer" == this.returnType.type && "java.util.List" == this.returnType.className ? e.asList(o[0]) : void 0;
        }));
      })), ignoreError((function() {
        return JavaHelper.hookMethods("com.google.android.gms.org.conscrypt.Platform", "checkServerTrusted", (function(e, r) {
          Log.d("Bypassing Platform checkServerTrusted {1}");
        }));
      })), ignoreError((function() {
        return JavaHelper.hookMethods("com.android.org.conscrypt.Platform", "checkServerTrusted", (function(e, r) {
          Log.d("Bypassing Platform checkServerTrusted {2}");
        }));
      }));
    }));
  }, e;
}();

exports.AndroidHelper = e;

},{}],3:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: !0
}), exports.CHelper = void 0;

var t = function() {
  function t() {
    this.$funcCaches = {};
  }
  return Object.defineProperty(t.prototype, "dlopen", {
    get: function() {
      return this.getExportFunction(null, "dlopen", "pointer", [ "pointer", "int" ]);
    },
    enumerable: !1,
    configurable: !0
  }), t.prototype.getExportFunction = function(t, e, r, n) {
    var o = (t || "") + "|" + e;
    if (o in this.$funcCaches) return this.$funcCaches[o];
    var a = Module.findExportByName(t, e);
    if (null === a) throw Error("cannot find " + e);
    return this.$funcCaches[o] = new NativeFunction(a, r, n), this.$funcCaches[o];
  }, t.prototype.hookFunctionWithCallbacks = function(t, e, r) {
    var n = Module.findExportByName(t, e);
    if (null === n) throw Error("cannot find " + e);
    var o = {
      get: function(t, r, n) {
        return "name" === r ? e : t[r];
      }
    }, a = {};
    "onEnter" in r && (a.onEnter = function(t) {
      r.onEnter.call(new Proxy(this, o), t);
    }), "onLeave" in r && (a.onLeave = function(t) {
      r.onLeave.call(new Proxy(this, o), t);
    });
    var i = Interceptor.attach(n, a);
    return Log.i("Hook function: " + e + " (" + n + ")"), i;
  }, t.prototype.hookFunction = function(t, e, r, n, o) {
    var a = this.getExportFunction(t, e, r, n);
    if (null === a) throw Error("cannot find " + e);
    var i = n;
    Interceptor.replace(a, new NativeCallback((function() {
      for (var t = this, i = [], s = 0; s < n.length; s++) i[s] = arguments[s];
      var c = new Proxy(a, {
        get: function(o, a, i) {
          switch (a) {
           case "name":
            return e;

           case "argumentTypes":
            return n;

           case "returnType":
            return r;

           case "context":
            return t.context;

           default:
            o[a];
          }
        },
        apply: function(t, e, r) {
          return t.apply(null, r[0]);
        }
      });
      return o.call(c, i);
    }), r, i)), Log.i("Hook function: " + e + " (" + a + ")");
  }, t.prototype.getEventImpl = function(t) {
    var e = new function() {
      for (var e in this.method = !0, this.thread = !1, this.stack = !1, this.args = !1, 
      this.extras = {}, t) e in this ? this[e] = t[e] : this.extras[e] = t[e];
    }, r = function(t) {
      var r = {};
      for (var n in e.extras) r[n] = e.extras[n];
      e.method && (r.method_name = this.name), e.thread && (r.thread_id = Process.getCurrentThreadId()), 
      e.args && (r.args = pretty2Json(t), r.result = null, r.error = null);
      try {
        var o = this(t);
        return e.args && (r.result = pretty2Json(o)), o;
      } catch (t) {
        throw e.args && (r.error = pretty2Json(t)), t;
      } finally {
        if (e.stack) {
          for (var a = [], i = Thread.backtrace(this.context, Backtracer.ACCURATE), s = 0; s < i.length; s++) a.push(DebugSymbol.fromAddress(i[s]).toString());
          r.stack = a;
        }
        send({
          $event: r
        });
      }
    };
    return r.onLeave = function(t) {
      var r = {};
      for (var n in e.extras) r[n] = e.extras[n];
      if (1 == e.method && (r.method_name = this.name), !0 === e.thread && (r.thread_id = Process.getCurrentThreadId()), 
      !0 === e.args && (r.result = pretty2Json(t)), !0 === e.stack) {
        for (var o = [], a = Thread.backtrace(this.context, Backtracer.ACCURATE), i = 0; i < a.length; i++) o.push(DebugSymbol.fromAddress(a[i]).toString());
        r.stack = o;
      }
      send({
        $event: r
      });
    }, r;
  }, t;
}();

exports.CHelper = t;

},{}],4:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: !0
}), exports.IOSHelper = void 0;

var t = function() {
  function t() {}
  return t.prototype.bypassSslPinning = function() {
    Log.w("iOS Bypass ssl pinning");
    try {
      Module.ensureInitialized("libboringssl.dylib");
    } catch (t) {
      Log.d("libboringssl.dylib module not loaded. Trying to manually load it."), Module.load("libboringssl.dylib");
    }
    var t = new NativeCallback((function(t, i) {
      return Log.d("custom SSL context verify callback, returning SSL_VERIFY_NONE"), 0;
    }), "int", [ "pointer", "pointer" ]);
    try {
      CHelper.hookFunction("libboringssl.dylib", "SSL_set_custom_verify", "void", [ "pointer", "int", "pointer" ], (function(i) {
        return Log.d("SSL_set_custom_verify(), setting custom callback."), i[2] = t, this(i);
      }));
    } catch (i) {
      CHelper.hookFunction("libboringssl.dylib", "SSL_CTX_set_custom_verify", "void", [ "pointer", "int", "pointer" ], (function(i) {
        return Log.d("SSL_CTX_set_custom_verify(), setting custom callback."), i[2] = t, 
        this(i);
      }));
    }
    CHelper.hookFunction("libboringssl.dylib", "SSL_get_psk_identity", "pointer", [ "pointer" ], (function(t) {
      return Log.d('SSL_get_psk_identity(), returning "fakePSKidentity"'), Memory.allocUtf8String("fakePSKidentity");
    }));
  }, t;
}();

exports.IOSHelper = t;

},{}],5:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: !0
}), exports.JavaHelper = void 0;

var e = function() {
  function e() {}
  return Object.defineProperty(e.prototype, "classClass", {
    get: function() {
      return Java.use("java.lang.Class");
    },
    enumerable: !1,
    configurable: !0
  }), Object.defineProperty(e.prototype, "stringClass", {
    get: function() {
      return Java.use("java.lang.String");
    },
    enumerable: !1,
    configurable: !0
  }), Object.defineProperty(e.prototype, "threadClass", {
    get: function() {
      return Java.use("java.lang.Thread");
    },
    enumerable: !1,
    configurable: !0
  }), Object.defineProperty(e.prototype, "throwableClass", {
    get: function() {
      return Java.use("java.lang.Throwable");
    },
    enumerable: !1,
    configurable: !0
  }), Object.defineProperty(e.prototype, "uriClass", {
    get: function() {
      return Java.use("android.net.Uri");
    },
    enumerable: !1,
    configurable: !0
  }), Object.defineProperty(e.prototype, "urlClass", {
    get: function() {
      return Java.use("java.net.URL");
    },
    enumerable: !1,
    configurable: !0
  }), Object.defineProperty(e.prototype, "mapClass", {
    get: function() {
      return Java.use("java.util.Map");
    },
    enumerable: !1,
    configurable: !0
  }), Object.defineProperty(e.prototype, "applicationContext", {
    get: function() {
      return Java.use("android.app.ActivityThread").currentApplication().getApplicationContext();
    },
    enumerable: !1,
    configurable: !0
  }), e.prototype.isArray = function(e) {
    return !!(e.hasOwnProperty("class") && e.class instanceof Object && e.class.hasOwnProperty("isArray") && e.class.isArray());
  }, e.prototype.findClass = function(e, t) {
    if (void 0 === t && (t = void 0), void 0 === t || null == t) {
      if (parseInt(Java.androidVersion) < 7) return Java.use(e);
      var r = null, a = Java.enumerateClassLoadersSync();
      for (var o in a) try {
        var n = this.findClass(e, a[o]);
        if (null != n) return n;
      } catch (e) {
        null == r && (r = e);
      }
      throw r;
    }
    var s = Java.classFactory.loader;
    try {
      return Reflect.set(Java.classFactory, "loader", t), Java.use(e);
    } finally {
      Reflect.set(Java.classFactory, "loader", s);
    }
  }, e.prototype.$getClassName = function(e) {
    var t = e.$className;
    if (null != t) return t;
    if (null != (t = e.__name__)) return t;
    if (null != e.$classWrapper) {
      if (null != (t = e.$classWrapper.$className)) return t;
      if (null != (t = e.$classWrapper.__name__)) return t;
    }
    Log.e("Cannot get class name: " + e);
  }, e.prototype.$getClassMethod = function(e, t) {
    var r = e[t];
    return void 0 !== r || "$" == t[0] && void 0 !== (r = e["_" + t]) ? r : void 0;
  }, e.prototype.$defineMethodProperties = function(e) {
    Object.defineProperties(e, {
      className: {
        configurable: !0,
        enumerable: !0,
        writable: !1,
        value: this.$getClassName(e.holder)
      },
      name: {
        configurable: !0,
        enumerable: !0,
        get: function() {
          var e = this.returnType.className, t = this.className + "." + this.methodName, r = "";
          if (this.argumentTypes.length > 0) {
            r = this.argumentTypes[0].className;
            for (var a = 1; a < this.argumentTypes.length; a++) r = r + ", " + this.argumentTypes[a].className;
          }
          return e + " " + t + "(" + r + ")";
        }
      },
      toString: {
        configurable: !0,
        value: function() {
          return this.name;
        }
      }
    });
  }, e.prototype.$hookMethod = function(e, t) {
    if (void 0 === t && (t = null), null != t) {
      var r = new Proxy(e, {
        apply: function(e, t, r) {
          var a = r[0], o = r[1];
          return e.apply(a, o);
        }
      });
      e.implementation = function() {
        return t.call(r, this, Array.prototype.slice.call(arguments));
      }, Log.i("Hook method: " + e);
    } else e.implementation = null, Log.i("Unhook method: " + e);
  }, e.prototype.hookMethod = function(e, t, r, a) {
    void 0 === a && (a = null);
    var o = t;
    if ("string" == typeof o) {
      var n = o, s = e;
      "string" == typeof s && (s = this.findClass(s));
      var i = this.$getClassMethod(s, n);
      if (void 0 === i) return void Log.w("Cannot find method: " + this.$getClassName(s) + "." + n);
      if (null != r) {
        var l = r;
        for (var u in l) "string" != typeof l[u] && (l[u] = this.$getClassName(l[u]));
        o = i.overload.apply(i, l);
      } else {
        if (1 != i.overloads.length) throw Error(this.$getClassName(s) + "." + n + " has too many overloads");
        o = i.overloads[0];
      }
    }
    this.$defineMethodProperties(o), this.$hookMethod(o, a);
  }, e.prototype.hookMethods = function(e, t, r) {
    void 0 === r && (r = null);
    var a = e;
    "string" == typeof a && (a = this.findClass(a));
    var o = this.$getClassMethod(a, t);
    if (void 0 !== o) for (var n = 0; n < o.overloads.length; n++) {
      var s = o.overloads[n];
      void 0 !== s.returnType && void 0 !== s.returnType.className && (this.$defineMethodProperties(s), 
      this.$hookMethod(s, r));
    } else Log.w("Cannot find method: " + this.$getClassName(a) + "." + t);
  }, e.prototype.hookAllConstructors = function(e, t) {
    void 0 === t && (t = null);
    var r = e;
    "string" == typeof r && (r = this.findClass(r)), this.hookMethods(r, "$init", t);
  }, e.prototype.hookAllMethods = function(e, t) {
    void 0 === t && (t = null);
    var r = e;
    "string" == typeof r && (r = this.findClass(r));
    for (var a = [], o = r.class; null != o && "java.lang.Object" !== o.getName(); ) {
      for (var n = o.getDeclaredMethods(), s = 0; s < n.length; s++) {
        var i = n[s].getName();
        a.indexOf(i) < 0 && (a.push(i), this.hookMethods(r, i, t));
      }
      o = Java.cast(o.getSuperclass(), this.classClass);
    }
  }, e.prototype.hookClass = function(e, t) {
    void 0 === t && (t = null);
    var r = e;
    "string" == typeof r && (r = this.findClass(r)), this.hookAllConstructors(r, t), 
    this.hookAllMethods(r, t);
  }, e.prototype.getEventImpl = function(e) {
    var t = this, r = new function() {
      for (var t in this.method = !0, this.thread = !1, this.stack = !1, this.args = !1, 
      this.extras = {}, e) t in this ? this[t] = e[t] : this.extras[t] = e[t];
    };
    return function(e, a) {
      var o = {};
      for (var n in r.extras) o[n] = r.extras[n];
      r.method && (o.class_name = e.$className, o.method_name = this.name, o.method_simple_name = this.methodName), 
      r.thread && (o.thread_id = Process.getCurrentThreadId(), o.thread_name = t.threadClass.currentThread().getName()), 
      r.args && (o.args = pretty2Json(a), o.result = null, o.error = null);
      try {
        var s = this(e, a);
        return r.args && (o.result = pretty2Json(s)), s;
      } catch (e) {
        throw r.args && (o.error = pretty2Json(e)), e;
      } finally {
        r.stack && (o.stack = pretty2Json(t.getStackTrace())), send({
          $event: o
        });
      }
    };
  }, e.prototype.fromJavaArray = function(e, t) {
    var r = e;
    "string" == typeof r && (r = this.findClass(r));
    for (var a = [], o = Java.vm.getEnv(), n = 0; n < o.getArrayLength(t.$handle); n++) a.push(Java.cast(o.getObjectArrayElement(t.$handle, n), r));
    return a;
  }, e.prototype.getEnumValue = function(e, t) {
    var r = e;
    "string" == typeof r && (r = this.findClass(r));
    var a = r.class.getEnumConstants();
    a instanceof Array || (a = this.fromJavaArray(r, a));
    for (var o = 0; o < a.length; o++) if (a[o].toString() === t) return a[o];
    throw new Error("Name of " + t + " does not match " + r);
  }, e.prototype.getStackTrace = function() {
    for (var e = [], t = this.throwableClass.$new().getStackTrace(), r = 0; r < t.length; r++) e.push(t[r]);
    return e;
  }, e;
}();

exports.JavaHelper = e;

},{}],6:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: !0
}), exports.ObjCHelper = void 0;

var t = function() {
  function t() {}
  return t.prototype.$fixMethod = function(t, e) {
    var r = e.origImplementation || e.implementation, n = t.toString(), o = ObjC.selectorAsString(e.selector), i = ObjC.classes.NSThread.hasOwnProperty(o);
    Object.defineProperties(e, {
      className: {
        configurable: !0,
        enumerable: !0,
        get: function() {
          return n;
        }
      },
      methodName: {
        configurable: !0,
        enumerable: !0,
        get: function() {
          return o;
        }
      },
      name: {
        configurable: !0,
        enumerable: !0,
        get: function() {
          return (i ? "+" : "-") + "[" + n + " " + o + "]";
        }
      },
      origImplementation: {
        configurable: !0,
        enumerable: !0,
        get: function() {
          return r;
        }
      },
      toString: {
        value: function() {
          return this.name;
        }
      }
    });
  }, t.prototype.$hookMethod = function(t, e) {
    void 0 === e && (e = null), null != e ? (t.implementation = ObjC.implement(t, (function() {
      var r = this, n = Array.prototype.slice.call(arguments), o = n.shift(), i = n.shift(), a = new Proxy(t, {
        get: function(t, e, n) {
          return e in r ? r[e] : t[e];
        },
        apply: function(t, e, r) {
          var n = r[0], o = r[1];
          return t.origImplementation.apply(null, [].concat(n, i, o));
        }
      });
      return e.call(a, o, n);
    })), Log.i("Hook method: " + t)) : (t.implementation = t.origImplementation, Log.i("Unhook method: " + pretty2String(t)));
  }, t.prototype.hookMethod = function(t, e, r) {
    void 0 === r && (r = null);
    var n = t;
    if ("string" == typeof n && (n = ObjC.classes[n]), void 0 === n) throw Error('cannot find class "' + t + '"');
    var o = e;
    if ("string" == typeof o && (o = n[o]), void 0 === o) throw Error('cannot find method "' + e + '" in class "' + n + '"');
    this.$fixMethod(n, o), this.$hookMethod(o, r);
  }, t.prototype.hookMethods = function(t, e, r) {
    void 0 === r && (r = null);
    var n = t;
    if ("string" == typeof n && (n = ObjC.classes[n]), void 0 === n) throw Error('cannot find class "' + t + '"');
    for (var o = n.$ownMethods.length, i = 0; i < o; i++) {
      var a = n.$ownMethods[i];
      if (a.indexOf(e) >= 0) {
        var s = n[a];
        this.$fixMethod(n, s), this.$hookMethod(s, r);
      }
    }
  }, t.prototype.getEventImpl = function(t) {
    var e = this, r = new function() {
      for (var e in this.method = !0, this.thread = !1, this.stack = !1, this.args = !1, 
      this.extras = {}, t) e in this ? this[e] = t[e] : this.extras[e] = t[e];
    };
    return function(t, n) {
      var o = {};
      for (var i in r.extras) o[i] = r.extras[i];
      if (r.method && (o.class_name = new ObjC.Object(t).$className, o.method_name = this.name, 
      o.method_simple_name = this.methodName), r.thread && (o.thread_id = Process.getCurrentThreadId(), 
      o.thread_name = ObjC.classes.NSThread.currentThread().name().toString()), r.args) {
        for (var a = [], s = 0; s < n.length; s++) a.push(e.convert2ObjcObject(n[s]));
        o.args = pretty2Json(a), o.result = null, o.error = null;
      }
      try {
        var c = this(t, n);
        return r.args && (o.result = pretty2Json(e.convert2ObjcObject(c))), c;
      } catch (t) {
        throw r.args && (o.error = pretty2Json(t)), t;
      } finally {
        if (r.stack) {
          var h = [], l = Thread.backtrace(this.context, Backtracer.ACCURATE);
          for (s = 0; s < l.length; s++) h.push(DebugSymbol.fromAddress(l[s]).toString());
          o.stack = h;
        }
        send({
          $event: o
        });
      }
    };
  }, t.prototype.convert2ObjcObject = function(t) {
    return t instanceof NativePointer || "object" == typeof t && t.hasOwnProperty("handle") ? new ObjC.Object(t) : t;
  }, t;
}();

exports.ObjCHelper = t;

},{}]},{},[1])
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIm5vZGVfbW9kdWxlcy9icm93c2VyLXBhY2svX3ByZWx1ZGUuanMiLCJpbmRleC50cyIsImxpYi9hbmRyb2lkLnRzIiwibGliL2MudHMiLCJsaWIvaW9zLnRzIiwibGliL2phdmEudHMiLCJsaWIvb2JqYy50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTs7Ozs7OztBQ0tBLElBQUEsSUFBQTtFQUFBLFNBQUE7SUFFSSxLQUFBLFFBQVEsR0FDUixLQUFBLE9BQU8sR0FDUCxLQUFBLFVBQVUsR0FDVixLQUFBLFFBQVEsR0FDQSxLQUFBLFNBQVMsS0FBSzs7RUFrQzFCLE9BaENJLE9BQUEsZUFBSSxFQUFBLFdBQUEsU0FBSztTQUFUO01BQ0ksT0FBTyxLQUFLOzs7O01BR2hCLEVBQUEsVUFBQSxXQUFBLFNBQVM7SUFDTCxLQUFLLFNBQVMsR0FDZCxLQUFLLEVBQUUsb0JBQW9CO0tBRy9CLEVBQUEsVUFBQSxJQUFBLFNBQUUsR0FBYztJQUNSLEtBQUssVUFBVSxLQUFLLFNBQ3BCLEtBQUs7TUFBRSxNQUFNO1FBQUUsT0FBTztRQUFTLFNBQVM7O09BQWE7S0FJN0QsRUFBQSxVQUFBLElBQUEsU0FBRSxHQUFjO0lBQ1IsS0FBSyxVQUFVLEtBQUssUUFDcEIsS0FBSztNQUFFLE1BQU07UUFBRSxPQUFPO1FBQVEsU0FBUzs7T0FBYTtLQUk1RCxFQUFBLFVBQUEsSUFBQSxTQUFFLEdBQWM7SUFDUixLQUFLLFVBQVUsS0FBSyxXQUNwQixLQUFLO01BQUUsTUFBTTtRQUFFLE9BQU87UUFBVyxTQUFTOztPQUFhO0tBSS9ELEVBQUEsVUFBQSxJQUFBLFNBQUUsR0FBYztJQUNSLEtBQUssVUFBVSxLQUFLLFNBQ3BCLEtBQUs7TUFBRSxNQUFNO1FBQUUsT0FBTztRQUFTLFNBQVM7O09BQWE7S0FHakU7Q0F4Q0EsSUF3REEsSUFBQTtFQUFBLFNBQUE7RUFvQkEsT0FsQkksRUFBQSxVQUFBLE9BQUEsU0FBSyxHQUFtQjtJQUNwQixPQUFPLGlCQUFpQixZQUFZO01BQ2hD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Q0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUM1R0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQ25DQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUN4TkE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSIsImZpbGUiOiJnZW5lcmF0ZWQuanMiLCJzb3VyY2VSb290IjoiIn0=
