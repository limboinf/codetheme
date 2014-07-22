/**
 * Created by beginman on 14-6-6.
 */
$(function(){
    switchTags();
    var type = $.getUrlParam('type');
    if (type == 1){
        getFans();
        $('#myTab li:eq(3) a').tab('show');
    }else if(type == 2){
        getUs();
        $('#myTab li:eq(2) a').tab('show');
    }else{
        getThemes();
    }

})
UID=0
//更改用户信息
function changeUser(type){
    var title = '提示'
        switch (type){
            case 0:
                title='更改用户名';
                var obj=$('#us').text();
                break;
            case 1:
                title='修改邮箱';
                var obj=$('#email').text();
                break;
            case 2:
                title='更改性别';
                var obj=$('#sex').text();
                break;
            case 3:
                title='更改站点信息';
                var obj=$('#url').text();
                break;
            case 4:
                title='更改个人简介';
                var obj=$('#desc').text();
                break;
        }
        var content = "<p><input type='text' id='obj' value='"+obj+"'></p>";
        var art = $.dialog({
        title: title,
        lock: true,
        content: content,
        ok:function(){
            var obj = $('#obj').val().trim();
            (type<3 && obj) || type>=3 ? is_valid=true : is_valid=false;
            if(is_valid){
                var url = "/manage/user/change_userinfo/";
                $.post(url, {'obj': obj, 'type':type}, function(data) {
                    var r = data.evalJson();
                    if (r.response == 'ok') {
                        alert(r.data);
                        art.close();
                        location.reload();
                    } else {
                        $.dialog({title: '提示', lock: true, skin: 'white', content: '保存失败，请联系管理员' });
                    }
                })
            }else{
                alert('你忘填写啦');
            }
        },
        cancel: true
    });

}

// 删除主题
function delMs(id){
    if(confirm('确定要删除这条消息吗？')){
        var url = '/manage/user/del_ms/';
        $.post(url,{'id':id},function(data){
            data.evalJson().response == 'ok' ? location.reload(): alert('内什么，系统崩溃了');
        })
    }
}

// 切换标签页
function switchTags(){
    //$('#myTab li:eq(0) a').tab('show') // Select third tab (0-indexed)
    $('#myTab li:eq(0) a').click(function(){
        getThemes()
    })

    $('#myTab li:eq(1) a').click(function(){
        // 加载用户分享
        getShare();
    })
    $('#myTab li:eq(2) a').click(function(){
        // 加载用户关注的人
        getUs();
    })
    $('#myTab li:eq(3) a').click(function(){
        // 加载用户粉丝
        getFans();
    })

}

// 异步加载用户主题
function getThemes(){
    var uid = UID;
    var url = '/codetheme/get_user_status/';
    $.post(url,{'uid': uid, 'type':1}, function(data){
        $('#userTheme').html(data);
    })
}

// 异步加载用户分享
function getShare(){
    var uid = UID;
    var url = '/codetheme/get_user_status/';
    $.post(url,{'uid': uid,'type':2}, function(data){
        $('#userShare').html(data);
    })
}

// 异步加载用户关注的人
function getUs(){
    var uid = UID;
    var url = '/codetheme/get_user_status/';
    $.post(url,{'uid': uid, 'type':3}, function(data){
        $('#useryoulove').html(data);
    })
}

// 异步加载用户粉丝
function getFans(){
    var uid = UID;
    var url = '/codetheme/get_user_status/';
    $.post(url,{'uid': uid, 'type':4}, function(data){
        $('#userloveyou').html(data);
    })
}

// 标记为已读
function hasRead(m_id, elem){
    var url = '/manage/user/ms/read/';
    $.post(url, {'m_id': m_id}, function(data){
        var r = data.evalJson();
        if(r.response == 'ok'){
            $(elem).remove();
            $('#ms_'+m_id).attr('class', 'media alert-info');
        }else{
            alert('出错了，给管理员说说吧')
        }
    })
}
