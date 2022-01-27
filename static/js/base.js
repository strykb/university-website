$('.dropdown-submenu > a').on("click", function(e) {
    var submenu = $(this);
    $('.dropdown-submenu .dropdown-menu').removeClass('show');
    $('.dropdown-submenu .dropdown-menu').removeClass('d-block');
    submenu.next('.dropdown-menu').addClass('show');
    submenu.next('.dropdown-menu').addClass('d-block');
    e.stopPropagation();
  });
  
  $('.dropdown').on("hidden.bs.dropdown", function() {
    // hide any open menus when parent closes
    $('.dropdown-menu.show').removeClass('show');
    $('.dropdown-submenu .dropdown-menu').removeClass('d-block');
  });