//Helper function
function navigate() {
    window.location.href = '/home'   
};

//function to call create profile, and once the profile is created, then navigate to "home"
window.onload = function create_profile(){
    fetch('/create_profile').then(navigate)
};
//if someone tries to use the broswer to go back from home, insetead of being taken to the loading screen
//they are taken back to the profile page to create a new profile
window.addEventListener( "pageshow", function ( event ) {
    var historyTraversal = event.persisted || 
                           ( typeof window.performance != "undefined" && 
                                window.performance.navigation.type === 2 );
    if ( historyTraversal ) {
      // Handle page restore.
      window.location.replace('/');
    }
  });
//deletes all possible images generated when exiting
window.onbeforeunload = function delete_profile() {
fetch('/delete')
};
