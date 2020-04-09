$(document).ready(function () {
  $('#heroes, #players').change(function () {
    select1 = $('#heroes').val();
    select2 = $('#players').val();
    if (select1.length == 0 || select2.length == 0) {
        $('#submit').prop("disabled", true);
    }
    else {
        $('#submit').prop("disabled", false);
    }
  })
});
$(document).ready( function () {
    $('#winloss').DataTable({
        "paging": false,
        "searching": false,
        "stateSave": true,
        "stateDuration": 0
    });
} );
