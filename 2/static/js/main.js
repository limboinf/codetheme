// init
$(function ($) {
    choiceCode();
    choiceDate();
    setTree();
    addTheme();
})

//　添加分类
function addCode(elem) {
    var content = '	<div class="un_open">\
		<p><span class="fs14">分类名：</span> <input type="text" id="code" class="input" /></p>\
	</div>';
    $.dialog({
        title: '添加分类',
        lock: true,
        skin: 'white',
        content: content,
        ok:function(){
            var code = $('#code').val();
            if (code) {
                var url = "/manage/addcode/";
                $.post(url, {'code': code}, function(data) {
                    var r = data.evalJson();
                    if (r.response == 'ok') {
                        $(elem).before('<button type="button" class="btn btn-default" style="margin-right: 10px;display: block" id="c_'+ r.data+'">'+code+'</button>')
                        $('#c_'+ r.data).bind('click',choiceCode())
                    } else {
                        $.dialog({title: '提示', lock: true, skin: 'white', content: '保存失败，请联系管理员' });
                    }
                })
            } else {
                $.dialog({title: '提示',lock: true, skin: 'white', content: '请填写分类名称'});
            }
        },
        cancel: true
    });
}

// 选择方向效果
function choiceCode(){
    $('#codes button').click(function(){
        $('#codes button').attr('class','btn btn-default');
        $(this).addClass('btn btn-success');
    })
}

//日期范围选择
function choiceDate(){
    if($('#begin_date').length && $('#end_date').length){
        $('#begin_date').calendar({ maxDate:'#end_date' });
        $('#end_date').calendar({ minDate:'#begin_date' });

        $('#begin_date').bind('click',function(){
            $(this).calendar()
        })
        $('#end_date').bind('click',function(){
            $(this).calendar()
        })
    }

}

//添加标签
function addIt(elem){
    var tags = getTags();
    var title = $.trim(elem);
    if(jQuery.inArray( title, tags ) == -1){
        $('.bootstrap-tagsinput input').before('<span class="tag label label-info">'+title+'<span data-role="remove"></span></span>')
    }
    $('span[data-role="remove"]').bind('click',function(){
        $(this).parent().remove();
    })
}
//获取标签
function getTags(){
    var tags = new Array()
    $('.bootstrap-tagsinput span').each(function(){
        tags.push($(this).text())
    })
    return tags
}

//设置节点
function setTree(){

};




//发布编程主题
function addTheme(){
    $("#themeform").submit(function(e){
        e.preventDefault();
        var title = $.trim($('#title').val());
        if(!title){
            return alert('你忘了填写标题了');
        }
        var code = $('#codes').find('button.btn.btn-default.btn-success');
        if(!code.length){
            return alert('你需要明确一个方向')
        }
        var code = code.attr('id').split('_')[1];
        // 简介
        var desc = $('#desc').val();
        if(desc.length>1000){
            return alert('哥们，你也写得太多了吧。');
        }
        //　获取标签转换成字符串
        var tags = getTags();
        tags = JSON.stringify(tags);

        //日期时间
        var begin_date = $('#begin_date').val();
        var end_date = $('#end_date').val();
        var d1 = new Date(begin_date.replace(/\-/g, "\/"));
        var d2 = new Date(end_date.replace(/\-/g, "\/"));
        if(begin_date!=""&&end_date!=""&&d1 >d2){
            return alert("开始时间不能大于结束时间！");
         }
        //学习思路
        var map = ''
        // 保存标签
        var url = '/manage/addtheme/';
        datas = {'title': title,'code':code,'desc':desc,'tags':tags,'begin_date':begin_date,'end_date':end_date,'map':map}
        setBtn('off',$('#submit'),'发布主题');     //禁用按钮
        $.post(url,datas,function(data){
            var r = data.evalJson();
            if(r.response == 'ok'){
                location.href='/manage/';
            }else{
                alert('额..出错了!');
            }
        })
  });
}
// 删除theme
function delTheme(id){
    if(confirm('确定要删除它吗？')){
        var url = '/manage/theme/del/';
        $.post(url,{'id':id}, function (data) {
            var r = data.evalJson();
            if(r.response == 'ok'){
                $('#theme_'+id).remove();
            }else{
                alert('Oh,fuck!报错了')
            }
        })
    }
}

