$(document).ready(function() {
    $('#heroes, #players').change(function() {
        select1 = $('#heroes').val();
        select2 = $('#players').val();
        if (select1.length == 0 || select2.length == 0) {
            $('#submit').prop("disabled", !0)
        } else {
            $('#submit').prop("disabled", !1)
        }
    })
});
$(document).ready(function() {
    $('#winloss').DataTable({
        "paging": !0,
        "pageLength": 5,
        "lengthMenu": [
            [5, 10, -1],
            [5, 10, "All"]
        ],
        "searching": 0,
        "stateSave": 1,
        "stateDuration": 0
    })
});

$(document).ready(function(){
        if (/Android|webOS|iPhone|iPad|iPod|BlackBerry/i.test(navigator.userAgent)) {
            $('.selectpicker').selectpicker('mobile');
        }
    });

$('#reset').click(function(){
   $("[name=inline_radio]").prop("checked",false);
});


