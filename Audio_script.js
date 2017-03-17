var wavesurfer = WaveSurfer.create({
    container: '#waveform',
    waveColor: 'violet',
    progressColor: 'purple'
});

var identifiedSpeakers = [];
var index = 0;
var selectedEnrolledSpeaker = null;
var names = [];

/*wavesurfer.load(sessionStorage.getItem("file_name"));*/
if (sessionStorage.getItem("file_name") !== null) {
    wavesurfer.load(sessionStorage.getItem("file_name"));
} else {
    wavesurfer.load('Obama_Interview_16.wav');
}

wavesurfer.on('ready', function () {
    wavesurfer.enableDragSelection({
        loop: false,
        id: "speaking",
        
    });
    /*
    wavesurfer.addRegion({
        start: 2,
        end: 5,
        color: 'hsla(100, 100%, 30%, 0.1)'
    })*/
    
});

/*
When a new region is created, delete previous selection
*/
wavesurfer.on('region-created', function () {
    wavesurfer.clearRegions();
    document.getElementById("input_name").hidden = true;
});

/*
After a region is created or updated, enable the buttons that
allow the user to interact with the selections
*/
wavesurfer.on('region-update-end', function () {
    document.getElementById("playselection").disabled = false;
    document.getElementById("choose").disabled = false;
    document.getElementById("reset").disabled = false;
});

wavesurfer.on('finish', function () {
   docuemnt.getElementById("playpause").textContent = "Play"; 
});

/*
Toggles whether the audio is playing or paused and updates the text of the 
play/pause button to reflect the current state
*/
function clicked() {
    wavesurfer.playPause();
    if (wavesurfer.isPlaying()) {
        document.getElementById("playpause").textContent = "Pause";
    } else {
        document.getElementById("playpause").textContent = "Play";
    }
}

/*
Skips forward or backward one second
*/
function skipAround(direction) {
    wavesurfer.skip(direction);
}

/*
Plays the selected region. Stops at end of region
*/
function playselection() {
    var selection = wavesurfer.regions.list.speaking;
    wavesurfer.play(selection.start, selection.end);
    document.getElementById("playpause").textContent = "Pause";
}

/*
Returns page to its default conditions
*/
function reset() {
    wavesurfer.clearRegions();
    document.getElementById("playselection").disabled = true;
    document.getElementById("choose").disabled = true;
    document.getElementById("input_name").hidden = true;
    document.getElementById("label").value = "";
    document.getElementById("rectangle").hidden = false;
    document.getElementById("reset").disabled = true;
}
/*
Displays the input box for the user to input a name label for the selected audio
*/
function chooseSelection() {
    document.getElementById("input_name").hidden = false;
    document.getElementById("warn").innerHTML = "";
    document.getElementById("label").focus();
    document.getElementById("rectangle").hidden = true;
}


/*
Stores the data for a speaker profile in the identifiedSpeakers array
Each element in the identifiedSpeakers array is an array with the following format:
[name, start_time, end_time]
*/
function enrollSpeaker() {
    var name = document.getElementById("label").value;
    if (name == "") {
        document.getElementById("warn").innerHTML = "Please enter a name for the selection";
    } //else if (checkNames(name)) {
      //  document.getElementById("warn").innerHTML = "Name already assigned";  
    //} else {
    else {
        var x = wavesurfer.regions.list.speaking;
        var data = [name, x.start, x.end];
        identifiedSpeakers.push(data);
        reset();
        wavesurfer.seekTo(0);
    }
    document.getElementById("speakerList").hidden = false;
    displaySpeakers();
}

function checkNames(arg) {
    var ii;
    for (ii = 0; ii < names.length; ii++) {
        if (arg == names[ii]) {
            return true;
        }
    }
    return false;
}

function identify(arg) {
    var ii;
    var z = document.getElementById("identifiedSpeakers").childNodes;
    for (ii = 0; ii < names.length; ii++) {
        if (arg == names[ii]) {
            z[ii].style.borderColor = "blue";
            selectedEnrolledSpeaker = ii;
        } else {
            z[ii].style.borderColor = "black";
        }
    }
    
    document.getElementById("playenrolled").disabled = false;
    document.getElementById("removeselection").disabled = false;
    document.getElementById("transcribe").disabled = false;
}

function playEnrolled() {
    var x = identifiedSpeakers[selectedEnrolledSpeaker];
    //wavesurfer.addRegion("temp", x[1], x[2]);
    wavesurfer.play(x[1], x[2]);
    document.getElementById("playpause").textContent = "Pause";
}

function displaySpeakers() {
    var jj;
    var x = identifiedSpeakers[index];
    var labels = ['Name: ','Start: ','End: '];
    var node = document.createElement("button");
    node.name = x[0];
    names.push(x[0]);
    node.className = "dispSpeaker";
    var arg = index;
    node.onclick = function () { identify(this.name) };
    for (jj = 0; jj < 3; jj++) {
        if (jj == 0) {
            var textnode = document.createTextNode(labels[jj] + x[jj]);  
        } else {
            
            var textnode = document.createTextNode(labels[jj] + x[jj].toFixed(2) + 's');
        }
        node.appendChild(textnode);
        node.appendChild(document.createElement("br"));  
    }
    document.getElementById("identifiedSpeakers").appendChild(node);
    index++; 
}

function removeSelection() {
    document.getElementById("playenrolled").disabled = true;
    document.getElementById("removeselection").disabled = true;
    document.getElementById("transcribe").disabled = false;
    var z = document.getElementById("identifiedSpeakers");
    z.removeChild(z.childNodes[selectedEnrolledSpeaker]);
    names.splice(selectedEnrolledSpeaker, 1);
    identifiedSpeakers.splice(selectedEnrolledSpeaker, 1);
    index--;
    if (identifiedSpeakers.length == 0) {
        document.getElementById("speakerList").hidden = true;
    }
}

function transcribe() {
    var f = document.getElementById("finalsubmit");
    var ii;
    var jj;
    for (ii = 0; ii < identifiedSpeakers.length; ii++) {
        var x = identifiedSpeakers[ii];
        for (jj = 0; jj < 3; jj++) {
            var z = document.createElement("input");
            z.value = x[jj];
            z.type = "text";
            if (jj == 0) {
                z.name = "name" + ii;
            } else if (jj == 1) {
                z.name = "start" + ii;
            } else {
                z.name = "end" + ii;
            }
            f.appendChild(z);
        }
    }
    console.log(identifiedSpeakers);
    f.submit();
}
