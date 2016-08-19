init_calendar();

function init_calendar() {
	var date = new Date();
	var d = date.getDate();
	var m = date.getMonth();
	var y = date.getFullYear();

	var calendar = $('#calendar').fullCalendar({
		//isRTL: true,
		//firstDay: 1,// >> change first day of week
		lang: "zh-cn",
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
		events: [
		  {
			title: 'All Day Event\nlilei\n13:00~15:00',
			start: new Date(y, m, 1),
			className: 'label-important'
		  },
		  {
			title: 'Long Event\nlilei\n13:00~15:00',
			start: moment().subtract(0, 'days').format('YYYY-MM-DD'),
			end: moment().subtract(-5, 'days').format('YYYY-MM-DD'),
			className: 'label-success'
		  },
		  {
			title: 'Some Event',
			start: new Date(y, m, d-3, 16, 0),
			allDay: false,
			className: 'label-info'
		  }
		],
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
			var start_date = new Date(start);
			var end_date = new Date(end);
			var org_id = $.trim($("#org_id").val());
			var br_id = $.trim($("#br_id").val());
			if (br_id == ''){
				$.messager.popup('请先选择机构和会议室！');
				calendar.fullCalendar('unselect');
				return false;
			}
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
									<input name="start_date" type="text" class="form-control" id="start_date" value="'+start_date.getUTCHours()+':'+start_date.getUTCMinutes()+'">\
								</div>\
							</div>\
							<div class="form-group">\
								<label class="col-sm-2 control-label">结束日期</label>\
								<div class="col-sm-9">\
									<input name="end_date" type="text" class="form-control" id="end_date" value="'+end_date.getUTCHours()+':'+end_date.getUTCMinutes()+'">\
								</div>\
							</div>\
						</div>\
						<script>\
							var nowdate = new Date('+start+');\
							$("#start_date").datetimepicker({\
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
							$("#end_date").datetimepicker({\
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
								var desc = $('#desc').val();
								var view = $('#calendar').fullCalendar('getView');
								calendar.fullCalendar('renderEvent',
									{
										title: name+desc,
										start: start,
										end: end,
										className: 'label-info'
									},
									true // make the event "stick"
								);
							}
						}
					}
				}
			);

			calendar.fullCalendar('unselect');
		},
		eventClick: function (calEvent, jsEvent, view) {
			var start = new Date(calEvent.start);
			var end = new Date(calEvent.end);
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
									<input name="start_date" type="text" class="form-control" id="start_date" value="'+start.getUTCHours()+':'+start.getUTCMinutes()+'">\
								</div>\
							</div>\
							<div class="form-group">\
								<label class="col-sm-2 control-label">结束日期</label>\
								<div class="col-sm-9">\
									<input name="end_date" type="text" class="form-control" id="end_date" value="'+end.getUTCHours()+':'+end.getUTCMinutes()+'">\
								</div>\
							</div>\
						</div>\
						<script>\
							var nowdate = new Date('+calEvent.start+');\
							$("#start_date").datetimepicker({\
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
							$("#end_date").datetimepicker({\
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
								calEvent.title = $.trim($('#name').val()) + '\n' + $('#desc').val();
								//TODO 时间修改
								calendar.fullCalendar('updateEvent', calEvent);
							}
						},
						delete: {
							lable: '删除',
							className: 'btn-danger',
							callback: function () {
								calendar.fullCalendar('removeEvents', function (ev) {
									return (ev._id == calEvent._id);
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
			redirect_to("/");
		},
		success : function(data) {
			if (data.resultFlag == "success") {
				document.getElementById("br_id").innerHTML = "";
				var opt=document.createElement("option");
				opt.innerText="--请选择会议室--";
				opt.value="0";
				$("#br_id").append(opt);
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
			redirect_to("/");
		},
		success : function(data) {
			if (data.resultFlag == "success") {
				$("#calendar").fullCalendar('removeEvents');
				for(var index=0;index<data.meetings.length;index++) {
					var start_date = data.meetings[index]['start_date'];
					var start_time = data.meetings[index]['start_time'];
					var end_date = data.meetings[index]['end_date'];
					var end_time = data.meetings[index]['end_time'];

					var s_datetime = get_data_int(start_date, start_time);
					var e_datetime = get_data_int(end_date, end_time);
					debugger;
					$("#calendar").fullCalendar('renderEvent',
						{
							title: data.meetings[index]['name'],
							start: new Date(parseInt(s_datetime[0]), parseInt(s_datetime[1])-1, parseInt(s_datetime[2]), parseInt(s_datetime[3]), parseInt(s_datetime[4])-8),
							end: new Date(parseInt(e_datetime[0]), parseInt(e_datetime[1])-1, parseInt(e_datetime[2]), parseInt(e_datetime[3]), parseInt(e_datetime[5])-8),
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

function get_data_int(date_str, time_str){
	var date_list = date_str.split('-');
	var time_list = time_str.split(':');
	date_list = date_list.concat(time_list);
	return date_list;
}





