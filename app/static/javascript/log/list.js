// 加载数据
var json_data = '{"count": 3, "pages": 2, "current": 1, "logs": [{"uid": 123, "id": 1, "header": "header_info", "time": "11:22:33", "date": "2018-04-11", "query": "k=v", "method": "POST"}, {"uid": 321, "id": 2, "header": "header", "time": "22:11:33", "date": "2018-04-12", "query": "k=x", "method": "GET"}]}';
var titles = {'id':'编号', 'uid':'用户ID', 'method':'method', 'route':'route', 'header':'Header', 'query':'Query', 'date':'请求日期', 'time':'请求时间'}
// 页码生成函数
function PageCalculator(dataCount, totalPage, currentPage, show_page_size, linesCount) {
	var first = 1;
	var pre = (currentPage-1) <= 0 ? 1 : (currentPage-1);
	var pre_status = (currentPage == 1) ? 'disabled' : '';
	var next = (currentPage+1) <= totalPage ? (currentPage+1) : totalPage;
	var next_status = (currentPage == totalPage) ? 'disabled' : '';
	var last = totalPage;
	var page_start = Math.floor(currentPage/show_page_size)+1;
	var page_end = (Math.floor(currentPage/show_page_size)+10) > totalPage ? totalPage : (Math.floor(currentPage/show_page_size)+10);
	var html = '';
	    html += '<ul class="pagination">';
		html += '<li ng-class="page.style" ng-repeat="page in pageList" class="ng-scope"><a href="javascript:getDataAjax('+first+');" class="ng-binding">首页</a></li>';
		html += '<li ng-class="page.style" ng-repeat="page in pageList" class="ng-scope"><a '+pre_status+' href="javascript:getDataAjax('+pre+');" class="ng-binding">上一页</a></li>';
		for (var i = page_start; i <= page_end; i++) {
			var currentPage_status = (currentPage==i) ? 'active' : '';
			html += '<li ng-class="page.style" ng-repeat="page in pageList" class="ng-scope '+currentPage_status+'"><a href="javascript:getDataAjax('+i+');" class="ng-binding">'+i+'</a></li>';
		}
		html += '<li ng-class="page.style" ng-repeat="page in pageList" class="ng-scope"><a '+next_status+' href="javascript:getDataAjax('+next+');" class="ng-binding">下一页</a></li>';
		html += '<li ng-class="page.style" ng-repeat="page in pageList" class="ng-scope"><a href="javascript:getDataAjax('+last+');" class="ng-binding">尾页</a></li>';
		html += '</ul>';
		html += '<ul class="pagination ng-scope" ng-if="pageList[0]">';
		html += '<li class="page-count disabled"><span>共 <b class="ng-binding">'+dataCount+'</b> 条记录 / 共 <b class="ng-binding">'+totalPage+'</b> 页</span></li>';
		html += '</ul>';
	return html;
}

// 格式数据到表格
// json_str 返回的json数据
// show_page_size 显示的页码数量
// linesCount 显示的数据条数
function formate_data(json_str, show_page_size, linesCount) {
	var data = JSON.parse(json_str);
	// 加载列表
	// 表头
	var titles_html = '<tr>'; 
	$.each(titles, function(k, title) { titles_html += "<th>" + title + "</th>"; });
	titles_html += '</tr>';
	// 数据列表
	var list_html = ''; 
	list = data.logs;
	$.each(list, function(i, log) {
		list_html += '<tr>';
		$.each(titles, function(k, title) { list_html += "<td>" + log[k] + "</td>"; });
		list_html += '</tr>';
	});
	// 加载页码列表 默认显示10页，不够的有多少显示多少
	var dataCount = data.count; // 记录总数
	var totalPage = Math.ceil(dataCount/linesCount); // 总页数
	var currentPage = data.current; // 当前页
	// 页码列表 最多10个页码 每页显示1条记录
	var page_bar_html = PageCalculator(dataCount, totalPage, currentPage, show_page_size, linesCount);

	// -------show-------------------
	$('.log-table-thead').empty().append(titles_html);
	$('.log-table-tbody').empty().append(list_html);
	$('.page-bar').empty().append(page_bar_html);
	if (data.count==0) {
		alert_message('无数据！', "alert-danger", "alert-success");
		return ;
	}
}

// ajax获取数据列表
function getDataAjax(page) {
	var pageSize = 20;
	$.post("/ajaxlist", {page: page, pageSize: pageSize}, function(json_data){
		formate_data(json_data, 10, pageSize);
	});
}

// 搜索操作
$('.search-btn').click(function(){
	var searchkey = $('#searchkey').val();
	if (!!!searchkey) {
		alert('搜索关键词格式错误');
		return ;
	}
	$.post("/ajaxsearch", {searchkey: searchkey}, function(json_data){
		formate_data(json_data, 1, 1000);
	});
});

// 翻页操作
$('.ng-scope').click(function(){
	alert(11);
});

getDataAjax(1);