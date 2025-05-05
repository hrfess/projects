Java.perform(function () {
    var File = Java.use("java.io.File");
    var FileOutputStream = Java.use("java.io.FileOutputStream");
    var OutputStreamWriter = Java.use("java.io.OutputStreamWriter");
    var BufferedWriter = Java.use("java.io.BufferedWriter");

    var path = "/sdcard/method_trace.txt";  // Make sure this is writable
    var file = File.$new(path);
    var fos = FileOutputStream.$new(file, true); // true = append mode
    var osw = OutputStreamWriter.$new(fos);
    var writer = BufferedWriter.$new(osw);

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

                        // Write to file
                        writer.write(log);
                        writer.newLine();
                        writer.flush();

                        return overload.apply(this, arguments);
                    };
                });
            });
        } catch (e) {
            // Skip classes that throw
        }
    });
});
