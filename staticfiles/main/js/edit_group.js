const url = JSON.parse(document.getElementById('url').textContent);

$(document).ready(function () {
    $('#id_students').select2({
        ajax: {
            url: url,
            dataType: 'json',
            processResults: function (data) {
                return {
                    results: $.map(data, function (item) {
                        return {id: item.id, text: `${item.id} - ${item.first_name} ${item.last_name}`};
                    })
                };
            }
        },
        minimumInputLength: 1
    });
});