function checkUpload(){
    var x = document.getElementById("upload");
    var l = x.files.length;
    var len = x.files[l-1].name.length;
    var extension = x.files[l-1].name.substring(len-3);
    
    if (extension != "wav"){
        document.getElementById("submit").disabled = true;
        document.getElementById("warn").innerHTML = "Please upload a WAV file!";
    }
    else{
        document.getElementById("warn").innerHTML = "";
        document.getElementById("submit").disabled = false;
        sessionStorage.setItem("file_name", x.files[l-1].name);
        //document.getElementById("files").submit();
    }
    
}

function cont() {
    document.getElementById("files").submit();
}