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

// function getShortcut(shortcutId) {
//     $.ajax({
//         url : "/api/shortcut/" + shortcutId,
//         type : "GET",
//         dataType: 'json',
//
//         success : function(json) {
//             if (json.hasOwnProperty('error'))
//                 Materialize.toast(json.error, 4000);
//             else {
//                 var shortcut = json.success;
//                 //$('#shortcut-image').prepend($('<img>', {src: shortcut.image, width: '100%'}));
//                 $('#shortcut-image').prepend('<img src="' + shortcut.image + '" width="100%">');
//                 $('#shortcut-author-img').prepend($('<img>', {src: shortcut.author_img}));
//                 $('#shortcut-desc').prepend('<p>' + shortcut.description + '</p>')
//                 $('#shortcut-author-info').prepend('<div class="author">' + shortcut.author + '<div style="width: 100%"><button style="font-size: 13px; border-radius: 5px; margin: 0; padding-top: 0; line-height: 0; width: 67px; height: 22px;" class="btn-floating btn-small waves-effect waves-light">Obserwuj</button></div></div>');
//                 $('#author-follow-btn').attr("onclick", "follow(\'"+shortcut.author+"\')");
//                 if (shortcut.type == 'link') {
//                     $('#shortcut-link-btn').prepend('<a href="'+shortcut.link+'" target="_blank"><button class="waves-effect waves-light btn white lighten-1" style="color: black"> Przejdź do strony</button> </a>');
//                     if (shortcut.is_authenticated) {
//                         $('#clipboard-btn').prepend('<button class="waves-effect waves-light btn white lighten-1" style="color: black" onclick="addToClipboard('+shortcut.id+')">Do przeczytania</button>');
//                     }
//                 }
//                 $('#shortcut-social').prepend('<div class="fb-share-button" data-href="http://www.your-domain.com/your-page.html" data-layout="button_count"><a class="fb-xfbml-parse-ignore" target="_blank" href="https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Feverfit.com%2F&amp;src=sdkpreparse">Share</a> </div>')
//             }
//         },
//
//         error : function(xhr, errmsg, err) {
//             console.log(xhr.status + ": " + xhr.responseText);
//         }
//     });
// }

function getShortcut(shortcutId) {
    $.ajax({
        url : "/api/shortcut/" + shortcutId,
        type : "GET",

        success : function(resp) {
            if (resp.hasOwnProperty('error'))
                Materialize.toast(resp.error, 4000);
            else {
                $('#shortcut-content').html(resp);
            }
        },

        error : function(xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
}

function showShortcut(shortcut_id) {
     $('#shortcut-modal').openModal({
         ready: function () {
             getShortcut(shortcut_id);
         },
         complete: function() {
             // $('#shortcut-image').empty();
             // $('#shortcut-author-img').empty();
             // $('#shortcut-desc').empty();
             // $('#shortcut-author-info').empty();
             // $('#shortcut-link-btn').empty();
             // $('#clipboard-btn').empty();
             // $('#shortcut-social').empty();
             $('#shortcut-content').empty();
         }
     })
}

function getVideo(shortcutId) {
    $.ajax({
        url : "/api/video/" + shortcutId,
        type : "GET",

        success : function(resp) {
            if (resp.hasOwnProperty('error'))
                Materialize.toast(resp.error, 4000);
            else {
                $('#video-content').html(resp);
            }
        },

        error : function(xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
}

function showVideo(shortcut_id) {
     $('#video-modal').openModal({
         ready: function () {
             getVideo(shortcut_id);
         },
         complete: function() {
            $('#video-content').empty();
         }
     })
}
