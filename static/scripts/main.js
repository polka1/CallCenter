// Reload table on submit
if(typeof django == 'undefined') {
    var jq = jQuery;
} else {
    var jq = django.jQuery;
}

(function($){
    $(document).ready(function() {
    var update_cycle = null;

        $('#search_form').on('submit', function (event) {
            if (update_cycle !== null){clearInterval(update_cycle)}
            obj = $(this);
            var interval = $('input[name="update_time_sec"]').val();
            console.log(interval);
            update_form(event,obj)
        });

    function update_form (event, obj) {
            event.preventDefault();
            var more = obj;
            var dateTime = $('input[name="time_start_0"]').val() + ' ' + $('input[name="time_start_1"]').val();
            var interval = $('input[name="update_time_sec"]').val();
            console.log('[ajax-update_form]: ', interval);
            $.ajax(more.data('url'), {
                'type': 'GET',
                'async': true,
                'dataType': 'html',
                'data': {
                    'date_time': dateTime,
                    'interval': interval
                },
                'success': function (data) {
                    $('#search_table').html(data);
                },
                'error': function (xhr,status,error) {
                    console.log(error);
                },
                'complete': function () {
                    var form = $('#search_form');
                    update_cycle = setTimeout(function () {
                        form.submit()
                    }, interval*1000);
                }
            })
    }
});

})(jq);
