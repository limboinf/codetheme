// init
$(function ($) {
    choiceCode();
    choiceDate();
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
    if($('#id_start_date').length && $('#id_end_date').length){
        $('#id_start_date').calendar({ maxDate:'#id_end_date' });
        $('#id_end_date').calendar({ minDate:'#id_start_date' });

        $('#id_start_date').bind('click',function(){
            $(this).calendar()
        })
        $('#id_end_date').bind('click',function(){
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



//发布编程主题
function addTheme(){
    $('#submit').click(function(){
        var code = $('#codes').find('button.btn.btn-default.btn-success');
        if(!code.length){
            return alert('你需要明确一个方向')
        }
        var code = code.attr('id').split('_')[1];
        $('input[name="type"]').val(code);
        //　获取标签转换成字符串
        var tags = getTags();
        tags = JSON.stringify(tags);
        $('input[name="id_tag"]').val(tags);
        var title = $.trim($('#id_title').val());
        if(!title){
            return alert('你忘了填写标题了');
        }
        //日期时间
        var begin_date = $('#id_start_date').val();
        var end_date = $('#id_end_date').val();
        if(!begin_date || !end_date){
            return alert('忘写时间了，注意时间观念')
        }
        var d1 = new Date(begin_date.replace(/\-/g, "\/"));
        var d2 = new Date(end_date.replace(/\-/g, "\/"));
        if(begin_date!=""&&end_date!=""&&d1 >d2){
            return alert("开始时间不能大于结束时间！");
         }
        setBtn('off',$('#submit'),'发布主题');     //禁用按钮
        $("#themeform").submit();   // 表单提交
    })

}
// 删除theme
function delTheme(id){
    if(confirm('请慎重处理，因为它会删除与之关联的很多很多……？')){
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
