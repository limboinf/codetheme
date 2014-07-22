//maxentries，页数
//current_page，当前页数
//url，请求地址
function splpage(option){
	var opts =$.extend({
		inspanel:$('#inspanel'),
		panel:$('#splPage'),
		url:'',
		map:{},
		maxentries:1,
		items_per_page:1,
		num_display_entries:4,
		current_page: 0,
		num_edge_entries:1,
		link_to:"javascript:;",
		prev_text:"上一页",
		next_text:"下一页",
		ellipse_text:"...",
		prev_show_always:false,
		next_show_always:false,
		callback:callback
	},option||{});
	var maxentries = parseInt(opts.maxentries);
	if (!maxentries || maxentries == 1) {return};//只有一页情况不显示
	function callback(index) {
		opts.map.object_id.pageno = index+1;
		$.post(opts.url,opts.map.object_id,function(data){
			opts.inspanel.html(data);
		})
	}
	function numPages() {
		return Math.ceil(maxentries/opts.items_per_page);
	}
	function getInterval() {
		var ne_half = Math.ceil(opts.num_display_entries/2);
		var np = numPages();
		var upper_limit = np-opts.num_display_entries;
		var start = current_page>ne_half?Math.max(Math.min(current_page-ne_half, upper_limit), 0):0;
		var end = current_page>ne_half?Math.min(current_page+ne_half, np):Math.min(opts.num_display_entries, np);
		return [start,end];
	}
	function pageSelected(page_id, evt){
		current_page = page_id;
		drawLinks();
		var continuePropagation = opts.callback(page_id, panel);
		if (!continuePropagation) {
			if (evt.stopPropagation) {
				evt.stopPropagation();
			}
			else {
				evt.cancelBubble = true;
			}
		}
		return continuePropagation;
	}
	function drawLinks() {
		panel.empty();
		var interval = getInterval();
		var np = numPages();
		var getClickHandler = function(page_id) {
			return function(evt){ return pageSelected(page_id,evt); }
		}
		var appendItem = function(page_id, appendopts){
			page_id = page_id<0?0:(page_id<np?page_id:np-1);
			appendopts = $.extend({text:page_id+1, classes:""}, appendopts||{});
			if(page_id == current_page){
				var lnk = $("<span class='current'>"+(appendopts.text)+"</span>");
			}
			else
			{
				var lnk = $("<a>"+(appendopts.text)+"</a>")
					.bind("click", getClickHandler(page_id))
					.attr('href', opts.link_to.replace(/__id__/,page_id));
			}
			if(appendopts.classes){lnk.addClass(appendopts.classes);}
			panel.append(lnk);
		}
		if(opts.prev_text && (current_page > 0 || opts.prev_show_always)){
			appendItem(current_page-1,{text:opts.prev_text, classes:"prev"});
		}
		if (interval[0] > 0 && opts.num_edge_entries > 0)
		{
			var end = Math.min(opts.num_edge_entries, interval[0]);
			for(var i=0; i<end; i++) {
				appendItem(i);
			}
			if(opts.num_edge_entries < interval[0] && opts.ellipse_text)
			{
				$("<span>"+opts.ellipse_text+"</span>").appendTo(panel);
			}
		}
		for(var i=interval[0]; i<interval[1]; i++) {
			appendItem(i);
		}
		if (interval[1] < np && opts.num_edge_entries > 0)
		{
			if(np-opts.num_edge_entries > interval[1]&& opts.ellipse_text)
			{
				$("<span>"+opts.ellipse_text+"</span>").appendTo(panel);
			}
			var begin = Math.max(np-opts.num_edge_entries, interval[1]);
			for(var i=begin; i<np; i++) {
				appendItem(i);
			}
		}
		if(opts.next_text && (current_page < np-1 || opts.next_show_always)){
			appendItem(current_page+1,{text:opts.next_text, classes:"next"});
		}
	}
	var current_page = opts.current_page;
	maxentries = (!maxentries || maxentries < 0)?1:maxentries;
	opts.items_per_page = (!opts.items_per_page || opts.items_per_page < 0)?1:opts.items_per_page;
	var panel = opts.panel;
	this.selectPage = function(page_id){ pageSelected(page_id);}
	this.prevPage = function(){ 
		if (current_page > 0) {
			pageSelected(current_page - 1);
			return true;
		}
		else {
			return false;
		}
	}
	this.nextPage = function(){ 
		if(current_page < numPages()-1) {
			pageSelected(current_page+1);
			return true;
		}
		else {
			return false;
		}
	}
	drawLinks();
}