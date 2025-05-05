Java.perform(function () {
    var loaded_classes = Java.enumerateLoadedClassesSync();
    loaded_classes.forEach(function (className) {
        try {
            var klass = Java.use(className);
            var methods = klass.class.getDeclaredMethods();

            methods.forEach(function (method) {
                var methodName = method.getName();
                var overloads = klass[methodName].overloads;

                overloads.forEach(function (overload) {
                    overload.implementation = function () {
                        var log = "-> " + className + "." + methodName + "(";
                        for (var i = 0; i < arguments.length; i++) {
                            log += arguments[i];
                            if (i < arguments.length - 1) log += ", ";
                        }
                        log += ")";
                        send(log);
                        return overload.apply(this, arguments);
                    };
                });
            });
        } catch (e) {
            // Many classes will throw, we skip them
        }
    });
});
