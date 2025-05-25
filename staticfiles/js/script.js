$(document).ready(function() {
    $('#toggleSidebar').click(function() {
        $('#sidebar').toggleClass('-translate-x-full');
    });

    $('.autocomplete').select2({
        ajax: {
            url: '/search-members/',
            dataType: 'json',
            delay: 250,
            data: function(params) {
                return { q: params.term };
            },
            processResults: function(data) {
                return {
                    results: data.results.map(function(item) {
                        return { id: item.id, text: item.name + ' (' + item.phone + ')' };
                    })
                };
            }
        },
        minimumInputLength: 2
    });
});