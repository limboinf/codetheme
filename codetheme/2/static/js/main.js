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
    $('#begin_date').calendar({ maxDate:'#end_date' });
    $('#end_date').calendar({ minDate:'#begin_date' });

    $('#begin_date').bind('click',function(){
        $(this).calendar()
    })
    $('#end_date').bind('click',function(){
        $(this).calendar()
    })

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
    var to = false;
    $('#demo_q').keyup(function () {
        if(to) { clearTimeout(to); }
        to = setTimeout(function () {
            var v = $('#demo_q').val();
            $('#jstree_demo').jstree(true).search(v);
        }, 250);
    });

    $('#jstree_demo')
        .jstree({
            "core" : {
                "animation" : 0,
                "check_callback" : true,
                "themes" : { "stripes" : true },
                'data' : [
                       { "id" : "map1", "parent" : "#", "text" : "思路导航" },
                       { "id" : "map2", "parent" : "map1", "text" : "NO1.概要" },
                       { "id" : "map3", "parent" : "map1", "text" : "...." },
                    ]
            },
            "types" : {
                "#" : { "max_children" : 1, "max_depth" : 4, "valid_children" : ["root"] },
                "root" : { "valid_children" : ["default"] },
                "default" : {"icon" : "glyphicon glyphicon-file","valid_children" : ["default","file"] },
                "file" : { "icon" : "glyphicon glyphicon-file", "valid_children" : [] }
            },
            "plugins" : [ "contextmenu", "dnd", "state", "types", "wholerow" ]
        });
}

// 添加节点
function demo_create() {
    var ref = $('#jstree_demo').jstree(true);
    var sel = ref.get_selected();
    if(!sel.length) {
        return false;
    }
    sel = sel[0];
    sel = ref.create_node(sel, {"type":"default"});
    if(sel) {
        ref.edit(sel);
    }
};
//　重命名节点
function demo_rename() {
    var ref = $('#jstree_demo').jstree(true),
        sel = ref.get_selected();
    if(!sel.length) { return false; }
    sel = sel[0];
    ref.edit(sel);
};
//　删除节点
function demo_delete() {
    var ref = $('#jstree_demo').jstree(true),
        sel = ref.get_selected();
    if(!sel.length) { return false; }
    ref.delete_node(sel);
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
        var code = code.text()
        alert(code)
        // 简介
        var desc = $('#desc').val();
        //　获取标签转换成字符串
        var tags = getTags()
        alert(tags.stringify)
        //日期时间
        var begin_date = $('#begin_date').val();
        var end_date = $('#end_date').val();
        //学习思路

        // 保存标签
        var url = '/manage/addcode/';
        $.post(url,)
  });
}