var flag = 1;
var cookie = document.cookie;
var createdTime = Date.now();
var reactionTime = Date.now();
var radios = document.getElementsByName('answers');

function findAnswer(){
    let answer = "";

    for (var i = 0, length = radios.length; i < length; i++) {
      if (radios[i].checked) {
        // do whatever you want with the checked radio
        var selector = 'label[for=' + radios[i].id + ']';
        var label = document.querySelector(selector);
        var text = label.innerHTML;

        // only one radio can be logically checked, don't check the rest
        break;
      }
    }
    return text;
}

$(document).ready(function() {
    $("input:checkbox").on('click', function() {
      // in the handler, 'this' refers to the box clicked on
      let $box = $(this);
      if ($box.is(":checked")) {
        // the name of the box is retrieved using the .attr() method
        // as it is assumed and expected to be immutable
        let group = "input:checkbox[name='" + $box.attr("name") + "']";
        // the checked state of the group/box on the other hand will change
        // and the current value is retrieved using .prop() method
        $(group).prop("checked", false);
        $box.prop("checked", true);
      } else {
        $box.prop("checked", false);
      }
    });
    document.getElementById("audio_play").addEventListener("click", function(e) {
        let audio = document.getElementById("audio");
        audio.play();
        if(flag===1){
            reactionTime = Date.now();
            flag+=1;
        }
    }, false);
});

function sendData(){
    clickedTime=Date.now();
    let answer = findAnswer()
    responseTime=(clickedTime-createdTime)/1000;
    task = window.location.pathname.replaceAll('/','').replace('en','');
    lang = window.location.pathname.split('/')[1];
    console.log(reactionTime);

    fetch('/api/saveResult', {

        // Declare what type of data we're sending
        headers: {
          'Content-Type': 'application/json',
          "Cache-Control": "no-cache"
        },

        // Specify the method
        method: 'POST',

        // A JSON payload
        body: JSON.stringify({
            "cookie": cookie,
            "reactionTime": (reactionTime-createdTime)/1000,
            "responseTime": responseTime,
            "task": task,
            "answer": answer,
            "language": lang
        })
    }).then(function (response) { // At this point, Flask has printed our JSON
        return response.text();
    }).then(function (text) {

        console.log('POST response: ');

        // Should be 'OK' if everything was successful
        console.log(text);
    });
}


