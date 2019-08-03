$(document).ready(function(event) {
    $('#like-form').on('submit', function(e) {
        var pk = $(this).attr('value');
        $.ajax({
            type: 'POST',
            url: "/forum/post/" + pk + "/",
            data: { 'id': pk, 'csrfmiddlewaretoken': '{{ csrf_token }}' },
            dataType: 'json',
            success: function(response) {
                console.log(response);
                $('#like-section').html(response['form'])
                console.log($('#like-section').html(response['form']));
            },
            error: function(rs, e) {
                console.log(rs.responseText);
            },
        });
        e.preventDefault();
    });
});
