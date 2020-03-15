$(function() {
    var h = $(window).height();
    $('#content').css('display','none');
    $('#loader-bg ,#loader').height(h).css('display','block');
  });
   
  $(window).load(function () { //全ての読み込みが完了したら実行
    $('#loader-bg').delay(900).fadeOut(800);
    $('#loader').delay(600).fadeOut(300);
    $('#content').css('display', 'block');
  });
   
  //10秒たったら強制的にロード画面を非表示
  $(function(){
    setTimeout('stopload()',5000);
  });
   
  function stopload(){
    $('#content').css('display','block');
    $('#loader-bg').delay(900).fadeOut(800);
    $('#loader').delay(600).fadeOut(300);
  }