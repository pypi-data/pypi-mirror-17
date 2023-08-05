function addSubmenuButtons() {
// If a list has child-lists, add a button for dropdown-click.
  // For each list:
  $('#portlets-in-header .portletNavigationTree ul').each(function() {
    var llist = $(this)
    // Check for sublist:
    var sublist = llist.find('ul')
    if(sublist.length > 0) {
      // Add button:
      $('<a href="#" alt="Open submenu" class="submenuButton openSubmenu">V</a>')
      .insertBefore(llist.find('> li > div'))
      .css('float', 'right')
      .click(function(eve) {
        handleSubmenuButtonClick(eve)
      });
    }
  });
}
function handleScreenSizes(maxWidth) {
  if($('body').width() < maxWidth) {
    makeMainMenuMobileFriendly()
  }
  else {
    makeMainMenuDesktopFriendly()
  }
}
function handleSubmenuButtonClick(eve) {
// Toggle submenu-visibility and submenu-class.
  eve.preventDefault()
  var button = $(eve.target)
  if(button.hasClass('openSubmenu')) {
    button.removeClass('openSubmenu')
    button.addClass('closeSubmenu')
  }
  else {
    button.removeClass('closeSubmenu')
    button.addClass('openSubmenu')
  }
  button.find('~ ul').toggle()
}
function makeMainMenuMobileFriendly() {
  addSubmenuButtons()
}
function makeMainMenuDesktopFriendly() {
  removeSubmenuButtons()
}
function removeSubmenuButtons() {
  $('#portlets-in-header .portletNavigationTree submenuButton').remove()

}
(function($) {
  var maxWidth = 600
  $(document).ready(function() {
    handleScreenSizes(maxWidth)
  });
  $(window).resize(function() {
    handleScreenSizes(maxWidth)
  });
})(jQuery);
