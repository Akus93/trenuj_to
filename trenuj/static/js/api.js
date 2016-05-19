function follow(username) {
    $.ajax({
        url : "/api/follow/",
        type : "GET",
        data : { user: username},
        dataType: 'json',

        success : function(json) {
            if (json.hasOwnProperty('error'))
                Materialize.toast(json.error, 4000);
            else
                Materialize.toast(json.success, 4000);
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
        dataType: 'json',

        success : function(json) {
            if (json.hasOwnProperty('error'))
                Materialize.toast(json.error, 4000);
            else
                Materialize.toast(json.success, 4000);
        },

        error : function(xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
}