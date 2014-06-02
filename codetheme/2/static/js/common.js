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