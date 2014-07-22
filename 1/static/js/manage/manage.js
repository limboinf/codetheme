// init
$(function ($) {
    choiceCode();
    choiceTags();
    choiceStatus();
    getThemeList();
})
/***************************************
后台主题管理
****************************************/
// 选择标签效果
function choiceTags(){
    $('#tags button').click(function(){
        $('#tags button').attr('class','btn btn-default');
        $(this).addClass('btn btn-primary');
        getThemeList();
    })
}

//选择状态效果
function choiceStatus(){
    $('#status button').click(function(){
        $('#status button').attr('class','btn btn-default');
        $(this).addClass('btn btn-info');
        getThemeList();
    })
}

// 选择方向效果
function choiceCode(){
    $('#manage_codes button').click(function(){
        $('#manage_codes button').attr('class','btn btn-default');
        $(this).addClass('btn btn-success');
        getThemeList();
    })
}

//获取theme列表
function getThemeList(){
    var code = $('#manage_codes button.btn.btn-success').attr('id').split('_')[1];
    var tag = $('#tags button.btn.btn-primary').attr('id').split('_')[1];
    var status = $('#status button.btn.btn-info').attr('id').split('_')[1];
    var title = $('#searchTxt').val();
    var url = '/manage/theme/list/';
    var datas = {'code':code, 'tag':tag,'status':status,'title':title, 'pageno':1}
    $.post(url,datas,function(data){
        $('#inspanel').html(data);
    })
}