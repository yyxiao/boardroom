init_calendar();

Date.prototype.Format = function(fmt)
{ //author: meizz
  var o = {
    "M+" : this.getUTCMonth()+1,                 //月份
    "d+" : this.getUTCDate(),                    //日
    "h+" : this.getUTCHours(),                   //小时
    "m+" : this.getUTCMinutes(),                 //分
    "s+" : this.getUTCSeconds(),                 //秒
    "q+" : Math.floor((this.getUTCMonth()+3)/3), //季度
    "S"  : this.getUTCMilliseconds()             //毫秒
  };
  if(/(y+)/.test(fmt))
    fmt=fmt.replace(RegExp.$1, (this.getUTCFullYear()+"").substr(4 - RegExp.$1.length));
  for(var k in o)
    if(new RegExp("("+ k +")").test(fmt))
	  fmt = fmt.replace(RegExp.$1, (RegExp.$1.length==1) ? (o[k]) : (("00"+ o[k]).substr((""+ o[k]).length)));
  return fmt;
};
Date.prototype.FormatLocal = function(fmt)
{ //author: meizz
  var o = {
    "M+" : this.getMonth()+1,                 //月份
    "d+" : this.getDate(),                    //日
    "h+" : this.getHours(),                   //小时
    "m+" : this.getMinutes(),                 //分
    "s+" : this.getSeconds(),                 //秒
    "q+" : Math.floor((this.getMonth()+3)/3), //季度
    "S"  : this.getMilliseconds()             //毫秒
  };
  if(/(y+)/.test(fmt))
    fmt=fmt.replace(RegExp.$1, (this.getFullYear()+"").substr(4 - RegExp.$1.length));
  for(var k in o)
    if(new RegExp("("+ k +")").test(fmt))
	  fmt = fmt.replace(RegExp.$1, (RegExp.$1.length==1) ? (o[k]) : (("00"+ o[k]).substr((""+ o[k]).length)));
  return fmt;
};


function init_calendar() {
	var date = new Date();
	var d = date.getDate();
	var m = date.getMonth();
	var y = date.getFullYear();

	var calendar = $('#calendar').fullCalendar({
		//isRTL: true,
		//firstDay: 1,// >> change first day of week
		lang: "zh-cn",
		timezone: "Shanghai",
		minTime: "07:00:00",
		maxTime: "21:00:00",
		buttonHtml: {
			prev: '<i class="ace-icon fa fa-chevron-left"></i>',
			next: '<i class="ace-icon fa fa-chevron-right"></i>'
		},
		defaultView: 'agendaDay',
		header: {
			left: 'prev,next today',
			center: 'title',
			right: 'month,agendaWeek,agendaDay'
		},
		events: [],
		timeFormat: 'H:mm',
		editable: false,
		droppable: false,
		drop: function (date) {

			var originalEventObject = $(this).data('eventObject');
			var $extraEventClass = $(this).attr('data-class');
			var copiedEventObject = $.extend({}, originalEventObject);

			copiedEventObject.start = date;
			copiedEventObject.allDay = false;
			if ($extraEventClass) copiedEventObject['className'] = [$extraEventClass];

			$('#calendar').fullCalendar('renderEvent', copiedEventObject, true);
			if ($('#drop-remove').is(':checked')) {
				$(this).remove();
			}
		},
		selectable: true,
		selectHelper: true,
		select: function (start, end, allDay) {
			var org_id = $.trim($("#org_id").val());
			var br_id = $.trim($("#br_id").val());
			if (br_id == ''){
				$.messager.popup('请先选择会议室！');
				calendar.fullCalendar('unselect');
				return false;
			}
			var start_date = new Date(start).Format("yyyy-MM-dd hh:mm:ss");
			var end_date = new Date(end).Format("yyyy-MM-dd hh:mm:ss");
			bootbox.dialog({
					title: "会议信息",
					locale: 'zh_CN',
					message: '<p id="meeting_cue"></p>\
						<div class="form-horizontal">\
							<div class="form-group">\
								<label class="col-sm-2 control-label">会议主题</label>\
								<div class="col-sm-9">\
									<input name="name" type="text" class="form-control" id="name">\
								</div>\
							</div>\
							<div class="form-group">\
								<label class="col-sm-2 control-label">滚动文字</label>\
								<div class="col-sm-9">\
									<input name="desc" type="text" class="form-control" id="desc">\
								</div>\
							</div>\
							<div class="form-group">\
								<label class="col-sm-2 control-label">开始日期</label>\
								<div class="col-sm-9">\
									<input name="start_time" type="text" class="form-control" id="start_time" value="'+start_date.substring(11,16)+'">\
								</div>\
							</div>\
							<div class="form-group">\
								<label class="col-sm-2 control-label">结束日期</label>\
								<div class="col-sm-9">\
									<input name="end_time" type="text" class="form-control" id="end_time" value="'+end_date.substring(11,16)+'">\
								</div>\
							</div>\
						</div>\
						<script>\
							var nowdate = new Date('+start+');\
							$("#start_time").datetimepicker({\
								language: "zh-CN",\
								autoclose: true,\
								todayHighlight: true,\
								format: "hh:mm",\
								startDate: nowdate,\
								startView: 1,\
								minView: 0,\
								maxView: 1,\
								minuteStep: 30\
							});\
							$("#end_time").datetimepicker({\
								language: "zh-CN",\
								autoclose: true,\
								todayHighlight: true,\
								format: "hh:mm",\
								startDate: nowdate,\
								startView: 1,\
								minView: 0,\
								maxView: 1,\
								minuteStep: 30\
							});\
						</script>',
					buttons: {
						success: {
							label: "保存",
							className: "btn-success",
							callback: function () {
								var name = $.trim($('#name').val());
								var desc = $('#desc').val().replace('\n', '');
								$.ajax({
									type : "POST",
									url : "/meeting/add",
									data : {
										"room_id" : br_id,
										"org_id": org_id,
										"name": name,
										"desc": desc,
										"start_date": start_date.substring(0, 10),
										"end_date": end_date.substring(0, 10),
										"start_time": $("#start_time").val(),
										"end_time": $("#end_time").val()
									},
									error : function() {
										$.messager.popup("与服务器通信失败，请稍后重试！");
									},
									success : function(data) {
										if (data.success) {
											$.messager.popup("预订会议成功！");
											load_meeting();
										} else {
											$.messager.popup(data.error_msg);
										}
									}
								});
							}
						}
					}
				}
			);

			calendar.fullCalendar('unselect');
		},
		eventClick: function (calEvent, jsEvent, view) {
			var org_id = $.trim($("#org_id").val());
			var br_id = $.trim($("#br_id").val());
			if (br_id == ''){
				$.messager.popup('请先选择会议室！');
				calendar.fullCalendar('unselect');
				return false;
			}
			var start_date = new Date(calEvent.start).FormatLocal("yyyy-MM-dd hh:mm:ss");
			var end_date = new Date(calEvent.end).FormatLocal("yyyy-MM-dd hh:mm:ss");
			var title = calEvent.title;
			var id = parseInt(title.substring(1,title.indexOf(']')));
			var name = title.substring(title.indexOf(']')+1, title.indexOf(' '));
			var desc = title.substring(title.indexOf('\n')+1).substring(0, title.substring(title.indexOf('\n')+1).indexOf('\n'));

			bootbox.dialog({
					title: "会议信息",
					locale: 'zh_CN',
					message: '<p id="meeting_cue"></p>\
						<div class="form-horizontal">\
							<div class="form-group">\
								<label class="col-sm-2 control-label">会议主题</label>\
								<div class="col-sm-9">\
									<input name="name" type="text" class="form-control" id="name" value="'+name+'">\
								</div>\
							</div>\
							<div class="form-group">\
								<label class="col-sm-2 control-label">滚动文字</label>\
								<div class="col-sm-9">\
									<input name="desc" type="text" class="form-control" id="desc" value="'+desc+'">\
								</div>\
							</div>\
							<div class="form-group">\
								<label class="col-sm-2 control-label">开始时间</label>\
								<div class="col-sm-9">\
									<input name="start_time" type="text" class="form-control" id="start_time" value="'+start_date.substring(11,16)+'">\
								</div>\
							</div>\
							<div class="form-group">\
								<label class="col-sm-2 control-label">结束时间</label>\
								<div class="col-sm-9">\
									<input name="end_time" type="text" class="form-control" id="end_time" value="'+end_date.substring(11,16)+'">\
								</div>\
							</div>\
						</div>\
						<script>\
							var nowdate = new Date('+calEvent.start+');\
							$("#start_time").datetimepicker({\
								language: "zh-CN",\
								autoclose: true,\
								todayHighlight: true,\
								format: "hh:mm",\
								startDate: nowdate,\
								startView: 1,\
								minView: 0,\
								maxView: 1,\
								minuteStep: 30\
							});\
							$("#end_time").datetimepicker({\
								language: "zh-CN",\
								autoclose: true,\
								todayHighlight: true,\
								format: "hh:mm",\
								startDate: nowdate,\
								startView: 1,\
								minView: 0,\
								maxView: 1,\
								minuteStep: 30\
							});\
						</script>',
					buttons: {
						success: {
							label: '保存',
							className: 'btn-success',
							callback: function () {
								var name_new = $.trim($('#name').val());
								var desc_new = $('#desc').val();
								$.ajax({
									type : "POST",
									url : "/meeting/update",
									data : {
										"id": id,
										"room_id" : br_id,
										"org_id": org_id,
										"name": name_new,
										"desc": desc_new,
										"start_date": start_date.substring(0, 10),
										"end_date": end_date.substring(0, 10),
										"start_time": $("#start_time").val(),
										"end_time": $("#end_time").val()
									},
									error : function() {
										$.messager.popup("与服务器通信失败，请稍后重试！");
									},
									success : function(data) {
										if (data.success) {
											$.messager.popup("修改会议成功！");
											load_meeting();
										} else {
											$.messager.popup(data.error_msg);
										}
									}
								});
							}
						},
						delete: {
							lable: '删除',
							className: 'btn-danger',
							callback: function () {
								$.ajax({
									type : "POST",
									url : "/meeting/del",
									data : {
										"id": id
									},
									error : function() {
										$.messager.popup("与服务器通信失败，请稍后重试！");
									},
									success : function(data) {
										if (data.success) {
											$.messager.popup("删除会议成功！");
											load_meeting();
										} else {
											$.messager.popup(data.error_msg);
										}
									}
								});
							}
						},
						cancel: {
							label: '取消',
							className: 'btn-sm',
							callback: ''
						}
					}
					}
				);
			calendar.fullCalendar('unselect');
		}
	});
}

function load_br() {
	var org_id = $.trim($("#org_id").val());
	$.ajax({
		type : "POST",
		url : "/booking/list_by_org",
		data : {
			"org_id" : org_id
		},
		error : function() {
			$.messager.popup("与服务器通信失败，请稍后重试！");
		},
		success : function(data) {
			if (data.resultFlag == "success") {
				document.getElementById("br_id").innerHTML = "";
				var opt=document.createElement("option");
				opt.innerText="--请选择会议室--";
				opt.value="";
				opt.selected="selected";
				$("#br_id").append(opt);
				var all=document.createElement("option");
				all.innerText="该机构下所有会议室";
				all.value=0;
				$("#br_id").append(all);
				for(var index=0;index<data.brs.length;index++)
				{
					opt=document.createElement("option");
					opt.innerText=data.brs[index]['br_name'];
					opt.value=data.brs[index]['br_id'];
					$("#br_id").append(opt);
				}
			} else {
				$.messager.popup(data.error_msg);
			}
		}
	})
}

function load_meeting (){
	var org_id = $.trim($("#org_id").val());
	var br_id = $.trim($("#br_id").val());
	$.ajax({
		type : "POST",
		url : "/booking/list_by_br",
		data : {
			"org_id" : org_id,
			"br_id" : br_id
		},
		error : function() {
			$.messager.popup("与服务器通信失败，请稍后重试！");
		},
		success : function(data) {
			if (data.resultFlag == "success") {
				$("#calendar").fullCalendar('removeEvents');
				for(var index=0;index<data.meetings.length;index++) {
					var id = data.meetings[index]['id'];
					var name = data.meetings[index]['name'];
					var desc = data.meetings[index]['description'];
					var create_user = data.meetings[index]['create_user'];
					var room_name = data.meetings[index]['room_name'];
					var start_date = data.meetings[index]['start_date'];
					var start_time = data.meetings[index]['start_time'];
					var end_date = data.meetings[index]['end_date'];
					var end_time = data.meetings[index]['end_time'];

					var title = '[' + id + ']' + name + ' ' + room_name +'\n' + desc + '\n' + create_user;
					var s_datetime = get_date_time(start_date, start_time);
					var e_datetime = get_date_time(end_date, end_time);
					$("#calendar").fullCalendar('renderEvent',
						{
							title: title,
							start: new Date(parseInt(s_datetime[0]), parseInt(s_datetime[1])-1, parseInt(s_datetime[2]), parseInt(s_datetime[3]), parseInt(s_datetime[4])),
							end: new Date(parseInt(e_datetime[0]), parseInt(e_datetime[1])-1, parseInt(e_datetime[2]), parseInt(e_datetime[3]), parseInt(e_datetime[4])),
							allDay: false,
							className: 'label-info'
						},
						true // make the event "stick"
					);
				}
			} else {
				$.messager.popup(data.error_msg);
			}
		}
	})
}

function get_date_time(date_str, time_str){
	var date_list = date_str.split('-');
	var time_list = time_str.split(':');
	date_list = date_list.concat(time_list);
	return date_list;
}

