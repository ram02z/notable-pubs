$(document).ready(function() {
    $('#heroes, #players').change(function() {
        select1 = $('#heroes').val();
        select2 = $('#players').val();
        select3 = $('#matchup').val();
        if (select1.length == 0 || select2.length == 0) {
            $('#submit_button').prop("disabled", !0)
            $('#refine').prop("disabled", !0)
        } else {
            $('#submit_button').prop("disabled", !1)
            $('#refine').prop("disabled", !1)
        }
    })
});
$(document).ready(function() {
  select2 = $('#players').val();
  $('#heroes').on('change', function() {
  if (select2.length == 0){
    document.title = 'Updating player select to match hero selection'
    loading();
    document.forms["form"].submit();
  }
  });
});

function loading(){
    $('#content').fadeOut();
    $('#content').hide();
    $('#loading').css('opacity', 0)
    $('#loading').show();
    $('#loading').animate(
        { opacity: 1 },
        { queue: false, duration: 400 });
    setTimeout(function() {
        $('#toolong').fadeIn("fast");
    }, 5000);
    setTimeout(function() {
        $('#toolong').html("Taking longer than expected (ᴗ˳ᴗ)");
        $('#toolong').fadeIn("fast");
    }, 10000);
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

$(document).ready(function(){
        if (/Android|webOS|iPhone|iPad|iPod|BlackBerry/i.test(navigator.userAgent)) {
            $('.selectpicker').selectpicker('mobile');
        };
});
$('#radio4').change(function(){
   var lenplayers = $('#players > option').length;
   $('#players').data('max-options', lenplayers).selectpicker('refresh');;
   $("#matchup").val('').trigger('change').selectpicker('refresh');
   $(".bs-select-all").prop('disabled', false);
   $("#players").selectpicker('refresh');
   $('#matchup-wrapper').collapse('hide');
   $("#matchup").prop("disabled",true).selectpicker('refresh');
});

$('.show-matchup').on('change', function() {
  var lenplayers2 = Math.floor(($('#players > option').length)/4);
  if (lenplayers2 < 5){
    var lenplayers2 = 5
  }
  $("#matchup").prop("disabled",false).selectpicker('refresh');
  $(".bs-select-all").prop('disabled', true);
  $("#players").selectpicker('refresh');
  $('#players').data('max-options', lenplayers2).selectpicker('refresh');
  var data=[];
  var $el=$("#players");
  $el.find('option:selected').each(function(){
    data.push($(this).val());
   });
  var handicap = data.slice(0,lenplayers2)
  $('#players').val(handicap).selectpicker('render');
  $("#matchup").val('').trigger('change').selectpicker('refresh');
  if($(this).val() === "Mid" || $(this).val() === "Off" || $(this).val() === "Safe"){
    $('#matchup-wrapper').collapse('show');
  }
});


$(document).ready(function() {
  $("[rel='tooltip'], .tooltip").tooltip();
  $('#winloss tbody').on('mouseover', 'tr', function() {
    $('[rel="tooltip"]').tooltip({
      trigger: 'hover',
      html: true
    });
  });
});


$('td').on('click','input',function() {
   $('.tooltip').tooltip('hide');
   $(this).select();
   document.execCommand('copy');
   var inp = $(this);
   var temp = $(this).val();
   $(this).val("Copied!");
   $(this).delay(800).fadeOut().fadeIn();
   setTimeout(function() {
        setID(inp, temp);
    }, 1200);
});

function setID(inp, temp){
    inp.val(temp);
}
$(document).ready(function() {
  $("#links-wrapper").css({
    'width': ($("#id-badge").width() + 10 + 'px')
  });
});

$('#id-badge').click(function(e){
    $('#links-wrapper').slideToggle(300,"swing");
});
$(document).ready(function() {
    $('.btn-group button').click(function() {
        $(this).prop('disabled', true).siblings().prop('disabled', false);
        var spanclass = "." + this.id
        $('#radspans > *').css('display','none');
        $('#direspans > *').css('display','none');
        $(spanclass).show();


    });
});