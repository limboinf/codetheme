$(function($){
webnav()
})

//按钮禁用与激活
function setBtn(type, obj,txt){
    if(type == 'off'){
        obj.text('正在处理中……');
        obj.attr('disabled','disabled')
    }else{
        obj.text(txt);
        obj.removeAttr('disabled');
    }
}

//导航
function webnav(){
    var path = window.location.pathname;
    if(path.indexOf('share') > -1){
        $('#webnav>li').removeClass();
        $('#share').addClass('active');
    };
    if(path.indexOf('codetheme') > -1){
        $('#webnav>li').removeClass();
        $('#codetheme').addClass('active');
    };
    if(path.indexOf('about') > -1){
        $('#webnav>li').removeClass();
        $('#about').addClass('active');
    }
}

// 加关注/取消关注
function loveUser(uid, elem) {
    var url = '/codetheme/loveuser/';
    var type = $(elem).text('加关注') ? 1 : 0;
    var txt = $(elem).text('加关注') ? '取消关注' : '加关注';
    $.post(url, {'uid':uid, 'type':type}, function(data){
        if(data == 'ok'){
            $(elem).text(txt);
        }else{
            alert('系统又抽了');
        }
    })
}

// 发私信
function sendMsOk(){
    var title = $('#msTitle').val().trim();
    var content = $('#msContent').val().trim();
    if (!title){
       return $('#ms_title').show();
    }else if(title.length>200){
        return $('#ms_title').show().text('*标题字数不超过200字');
    }else if(content.length>500){
        return $('#ms_content').show();
    }else{
        var who = $('#who').val();
        if(!who){
            return $('#ms_title').show().text('*没有接收人(告知管理员出现BUG啦)');
        }
        var url = '/codetheme/sendms/';
        $.post(url,{'title':title, 'content': content, 'who':who}, function(data){
            if(data == 'ok'){
                $('#s_ms_box').hide();
                $('#sendok').show(300);
            }
        })
    }
}


// 回复私信
function sendms(who){
    $('#who').val(who);

}
// 获取url参数
(function($){
    $.getUrlParam = function(name)
    {
        var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
        var r = window.location.search.substr(1).match(reg);
        if (r!=null) return unescape(r[2]); return null;
    }
})(jQuery);