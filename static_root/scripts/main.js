// Reload table on submit
if(typeof django == 'undefined') {
    var jq = jQuery;
} else {
    var jq = django.jQuery;
}

(function($){
    $(document).ready(function() {
    var update_cycle = null;

        $('#search_form').on('submit', function (evnt) {
            if (update_cycle !== null){clearTimeout(update_cycle)}
            update_cycle = setTimeout(update_form(evnt), 5000);
        });

    });

    function listening() {
            console.log("Set interval: "); // sanity check
            console.log($('#id_update_time_sec').val())
        }

    function update_form (event) {
            event.preventDefault();
            console.log("form submitted!");  // sanity check
            listening();
            var more = $(this);
            var dateTime = $('input[name="time_start_0"]').val() + ' ' + $('input[name="time_start_1"]').val();
            var interval = $('input[name="update_time_sec"]').val();
            console.log(dateTime, '\n', interval);
            console.log(more.data('url'));
            $.ajax(more.data('url'), {
                'type': 'GET',
                'async': true,
                'dataType': 'html',
                'data': {
                    'date_time': dateTime,
                    'interval': interval
                },
                'success': function (data) {
                    // console.log(data);
                    $('#search_table').html(data);
                    // for (var)
                },
                'error': function (xhr,status,error) {
                    console.log(error);
                }
            })

}})(jq);
