// init
$(function ($) {
    //LoveIt();
})

//　加关注
function LoveIt(id, elem) {
        var cs = $(elem).attr('class');
        var url = '/codetheme/love/';
        if(cs == 'btn btn-warning btn-xs'){
            // 关注
            $.post(url,{'id':id, 'type':1}, function(data){
                if(data == 'ok'){
                    $(elem).attr('class','btn btn-success btn-xs');
                    $('#love_'+id).text(parseInt($('#love_'+id).text())+1);
                }else{
                    alert('系统报错');
                }
            })
        }else{
            // 取消关注
             $.post(url,{'id':id, 'type':0}, function(data){
                if(data == 'ok'){
                    $(elem).attr('class','btn btn-warning btn-xs');
                    $('#love_'+id).text(parseInt($('#love_'+id).text())-1);
                }else{
                    alert('系统报错');
                }
            })
        }
}

