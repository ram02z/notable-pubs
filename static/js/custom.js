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
   var lenplayers = $('#players > option').length;
   $('#players').data('max-options', lenplayers).selectpicker('refresh');;
   $("#matchup").val('').trigger('change').selectpicker('refresh');
   $('#matchup-wrapper').collapse('hide');
   $("#matchup").prop("disabled",true).selectpicker('refresh');
});

$('.show-matchup').on('change', function() {
  $("#matchup").prop("disabled",false).selectpicker('refresh');
  $('#players').data('max-options', 3).selectpicker('refresh');
  var data=[];
  var $el=$("#players");
  $el.find('option:selected').each(function(){
    data.push($(this).val());
   });
  var handicap = data.slice(0,3)
  $('#players').val(handicap).selectpicker('render');
  $("#matchup").val('').trigger('change').selectpicker('refresh');
  if($(this).val() === "Mid" || $(this).val() === "Off" || $(this).val() === "Safe"){
    $('#matchup-wrapper').collapse('show');
  }
});
$(document).ready(function() {
    $("[rel='tooltip'], .tooltip").tooltip();
});

