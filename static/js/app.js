//init
//after window is loaded completely 
window.onload = function () {
  //hide the preloader
  setTimeout(function () {
    $('.loading-screen').fadeOut("fast");
  }, 0);
}

$(document).ready(function () {
  new WOW().init();
});
mTable = $('#myTable').DataTable({
  "paging": false,
  "scrollY": "390px",
  "scrollCollapse": true,
  "aaSorting": [],
    columnDefs: [{
      orderable: false,
      targets: [0, 1, 4]
    }],
  "dom": "lrtip"
});   //pay attention to capital D, which is mandatory to retrieve "api" datatables' object, as @Lionel said
$('#myInputTextField').keyup(function () {
  mTable.search($(this).val()).draw();
})

oTable = $('#myWatchTable').DataTable({
  "paging": false,
  "scrollY": "390px",
  "scrollCollapse": true,
  "aaSorting": [],
    columnDefs: [{
      orderable: false,
      targets: [0,3,4]
    }],
  "dom": "lrtip"
});   //pay attention to capital D, which is mandatory to retrieve "api" datatables' object, as @Lionel said
$('#myInputTextField').keyup(function () {
  oTable.search($(this).val()).draw();
})
//init


function goBack() {
  window.history.back();
}

function refreshPage() {
  window.location.reload();
}

function startpage() {
  window.location = "../";
}


$(document).ready(function () {
  $('#revealonhover').hover(function () {
    $('.reveal').addClass('animate__fadeInRight');
    $('.reveal').removeClass('animate__rotateOut animate__faster');
    $('.reveal').removeClass('d-none');
  },
    function () {
      $('.reveal').removeClass('animate__fadeInRight');
      $('.reveal').addClass('animate__rotateOut animate__faster');
      setTimeout(() => { $('.reveal').addClass('d-none'); }, 500);
      // $('.reveal').addClass('d-none');  
    });
});

jQuery(function ($) {
  $('#dropdownMenu2').click(function () {
    return true;
  }).dblclick(function () {
    window.location = "../";
    return false;
  });
});

$(document).ready(function () {
  $('.dropdown-submenu a.test').on("click", function (e) {
    $(this).next('ul').toggle();
    e.stopPropagation();
    e.preventDefault();
  });
});

$(document).on('click', '.confirm-delete', function(){
  return confirm('Add this movie to the Watch list?');
})


