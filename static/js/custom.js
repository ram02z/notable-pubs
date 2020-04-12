$(document).ready(function() {
    $('#heroes, #players').change(function() {
        select1 = $('#heroes').val();
        select2 = $('#players').val();
        select3 = $('#matchup').val();
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

$('#radio4').change(function(){
   $('#players').attr('multiple','multiple');
   $("#players").selectpicker('refresh');
   $("#matchup").val('').trigger('change');
   $('#matchup-wrapper').collapse('hide');
   $("#radio1").prop("checked",false);
   $("#radio2").prop("checked",false);
   $("#radio3").prop("checked",false);
   $("#matchup").prop("disabled",true);
   $("#matchup").selectpicker('refresh');
});

$('.show-matchup').on('change', function() {
  $("#matchup").prop("disabled",false);
  $("#matchup").selectpicker('refresh');
  $('#players').removeAttr('multiple');
  index = $('#players').prop('selectedIndex');
  $('#players option')[index].selected = true;
  $("#matchup").val('').trigger('change');
  if($(this).val() === "Mid" || $(this).val() === "Off" || $(this).val() === "Safe"){
    $('#matchup-wrapper').collapse('show');
  }
});
$(document).ready(function() {
    $("[rel='tooltip'], .tooltip").tooltip();
});

$(document).on('change', '.selectpicker', function () {
    $('.selectpicker').selectpicker('refresh');
});
