// Reload table on submit
$('#search_form').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!");  // sanity check
    listening();
});