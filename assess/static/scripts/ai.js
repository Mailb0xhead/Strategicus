// document.getElementById("aiPrompt").addEventListener("keydown",
// function(event) {
//     if (!event) {
//       var event = window.event;
//     }
//     if (event.keyCode == 13){
//       event.preventDefault();
//       ask_ai();
//     }
// }, false);

function csrfSafeMethod(method) {
// these HTTP methods do not require CSRF protection
return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});

function ask_ai(in_prompt) {
    var prompt = in_prompt;
    var form = new FormData();
    //   var aiprompt = document.getElementById("aiPrompt").value;
    // var airesponse =  document.getElementById("aiResponse").textContent;
    var aiprompt1 = "Tell me how I can " + prompt + " better.";
    var aiprompt2 = "This answer should consider all areas of that can help like books, websites, training or consulting partners."
    //   var newText = document.createElement("p");
    form.append("prompt_1", aiprompt1);
    form.append("prompt_2", aiprompt2);
    form.append("type", "action");
    // for (var key of form.entries()) {
    //  console.log(key[0] + ', ' + key[1]);
    // }
    var settings = {
        "url": "http://192.168.0.209:777/api/ai/",
        "method": "POST",
        "timeout": 0,
        "processData": false,
        "mimeType": "multipart/form-data",
        "contentType": false,
        "data": form,
    };

    $.ajax(settings).done(function (response) {
        console.log(response);

        let answer = JSON.parse(response);
        let text = answer.choices[0].text;

        document.getElementById("aiGuidance").innerHTML = text;

    });
};

