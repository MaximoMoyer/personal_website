//deletes all possible images generated when exiting
window.onbeforeunload = function delete_profile() {
    fetch('/delete')
  };

//if someone attempts to go back after hitting "create a new profile" this functions reloads the given page
//that is navigated to, to ensure that the default image is now shown everywhere.

//This avoids the case in which a users back spaces twice from the laoding screen
//in this case, without this function, the user would see their previous profile image on the first page they navigate back to
//then a default image going forward 

  window.addEventListener( "pageshow", function ( event ) {
    var historyTraversal = event.persisted || 
                           ( typeof window.performance != "undefined" && 
                                window.performance.navigation.type === 2 );
    if ( historyTraversal ) {
      // Handle page restore.
      window.location.reload();
    }
  });