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
//stack overflow: https://stackoverflow.com/questions/6453269/jquery-select-element-by-xpath
function _x(STR_XPATH) {
    var xresult = document.evaluate(STR_XPATH, document, null, XPathResult.ANY_TYPE, null);
    var xnodes = [];
    var xres;
    while (xres = xresult.iterateNext()) {
        xnodes.push(xres);
    }
    return xnodes;
}
function loading(){
    $("#loading").show();
    $(".alert").hide();
    $("#winloss").hide();
    $("#select-form").hide();
    $("#winloss_length").hide();
    $("#winloss_paginate").hide();
    $("#winloss_info").hide();
}
$(document).ready(function() {
    var table = $('#winloss').DataTable({
        "paging": !0,
        "pageLength": 6,
        "autoWidth": false,
        "columns": [
            { "width": "33.34%" },
            { "width": "33.33%" },
            { "width": "33.33%" }
          ],
        "lengthMenu": [ [6, 12, -1], [6, 12, "All"] ],
        "searching": 0
    });
});

$('#radio4').change(function(){
   var lenplayers = $('#players > option').length;
   $('#players').data('max-options', lenplayers).selectpicker('refresh');;
   $("#matchup").val('').trigger('change').selectpicker('refresh');
   $(_x('/html/body/div[1]/form/div[1]/div[2]/div/div/div[2]/div/button[1]')).prop('disabled', false);
   $("#players").selectpicker('refresh');
   $('#matchup-wrapper').collapse('hide');
   $("#matchup").prop("disabled",true).selectpicker('refresh');
});

$('.show-matchup').on('change', function() {
  $("#matchup").prop("disabled",false).selectpicker('refresh');
  $(_x('/html/body/div[1]/form/div[1]/div[2]/div/div/div[2]/div/button[1]')).prop('disabled', true);
  $("#players").selectpicker('refresh');
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
    $('#winloss tbody').on('mouseover', 'tr', function () {
    $('[rel="tooltip"]').tooltip({
        trigger: 'hover',
        html: true
    });
});
});

