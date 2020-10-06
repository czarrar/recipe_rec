// ----------
// # Parse URL
// -----------

// Let's get the query string
var QueryString = function () {
    // This function is anonymous, is executed immediately and
    // the return value is assigned to QueryString!
    var query_string = {};
    var query = window.location.search.substring(1);
    var vars = query.split("&");
    for (var i=0;i<vars.length;i++) {
        var pair = vars[i].split("=");
            // If first entry with this name
        if (typeof query_string[pair[0]] === "undefined") {
        query_string[pair[0]] = decodeURIComponent(pair[1]);
            // If second entry with this name
        } else if (typeof query_string[pair[0]] === "string") {
        var arr = [ query_string[pair[0]],decodeURIComponent(pair[1]) ];
        query_string[pair[0]] = arr;
            // If third or later entry with this name
        } else {
        query_string[pair[0]].push(decodeURIComponent(pair[1]));
        }
    }
    return query_string;
}();
// workerId
if (QueryString.workerId == undefined) {
    //alert('Please enter ?workerId=X into the url where X is some character/number');
}
var workId = QueryString.workerId;
var assId = QueryString.assignmentId;
var hitId = QueryString.hitId;
