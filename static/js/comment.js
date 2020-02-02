// hide show comments
function toggleComment(elem) {
  if($(elem).parent().siblings(".comment-block").css('display') == 'none') {
    $(elem).parent().siblings(".comment-block").css('display', 'block');
  } else {
    $(elem).parent().siblings(".comment-block").css('display', 'none');
  }
}
 