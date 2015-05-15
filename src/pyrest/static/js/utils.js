var now = Date.now();

function debug (msg) {
    var time = (Date.now() - now).toString();
    while (time.length < 5) time = " " + time;
    console.log (time + ': ' + msg);
}

function debugSocket (msg) {
    debug ('[s]: ' + msg);
}