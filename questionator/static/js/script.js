$(document).ready(function() {
  $(".previous").click(function() {
    $("#test > form").attr("action", $(this).attr("href"));
    $(this).removeAttr("href");
    $("#test > form").submit();
  });
});