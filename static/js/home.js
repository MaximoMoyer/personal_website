
//alters the text shown on "home" depending on the outcome of the image generation task
window.onload = function correct_display() { 
    if(document.getElementsByClassName('status')[0].id == "InvalidPrompt"){
    document.getElementById("header").innerHTML = "You submitted a prompt that the system did not like.";
    document.getElementById("lower").innerHTML = "So, until you create a more appropriate proflile, your image for today will be a toucan:";
    }
    else if (document.getElementsByClassName('sess_id')[0].id == 'default'){
    document.getElementById("header").innerHTML = "Profile image creation wasn't fully completed. ";
    document.getElementById("lower").innerHTML = "So for now, enjoy this toucan as your profile.";
    }
}