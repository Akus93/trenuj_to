function follow(username) {
    $.ajax({
        url : "/api/follow/",
        type : "GET",
        data : { user: username},

        success : function(json) {
            console.log(json);
        },

        error : function(xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
}

function addToClipboard(shortcutId) {
    $.ajax({
        url : "/api/clipboard/add/",
        type : "GET",
        data : { shortcut_id: shortcutId },

        success : function(json) {
            console.log(json);
        },

        error : function(xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
}