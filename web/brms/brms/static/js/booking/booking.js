init_calendar();

function init_calendar() {
	var date = new Date();
	var d = date.getDate();
	var m = date.getMonth();
	var y = date.getFullYear();
	var h = date.getHours();
	var mm = date.getMinutes();
	debugger;

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
		droppable: false, // this allows things to be dropped onto the calendar !!!
		drop: function (date) { // this function is called when something is dropped

			// retrieve the dropped element's stored Event Object
			var originalEventObject = $(this).data('eventObject');
			var $extraEventClass = $(this).attr('data-class');


			// we need to copy it, so that multiple events don't have a reference to the same object
			var copiedEventObject = $.extend({}, originalEventObject);

			// assign it the date that was reported
			copiedEventObject.start = date;
			copiedEventObject.allDay = false;
			if ($extraEventClass) copiedEventObject['className'] = [$extraEventClass];

			// render the event on the calendar
			// the last `true` argument determines if the event "sticks" (http://arshaw.com/fullcalendar/docs/event_rendering/renderEvent/)
			$('#calendar').fullCalendar('renderEvent', copiedEventObject, true);

			// is the "remove after drop" checkbox checked?
			if ($('#drop-remove').is(':checked')) {
				// if so, remove the element from the "Draggable Events" list
				$(this).remove();
			}

		}
		,
		selectable: true,
		selectHelper: true,
		select: function (start, end, allDay) {

			bootbox.prompt("会议名称:", function (title) {
				if (title !== null) {
					calendar.fullCalendar('renderEvent',
							{
								title: title,
								start: start,
								end: end,
								allDay: false,
								className: 'label-info'
							},
							true // make the event "stick"
					);
				}

			});

			calendar.fullCalendar('unselect');
		}
		,
		eventClick: function (calEvent, jsEvent, view) {

			//display a modal
			var modal =
					'<div class="modal fade">\
					  <div class="modal-dialog">\
					   <div class="modal-content">\
						 <div class="modal-body">\
						   <button type="button" class="close" data-dismiss="modal" style="margin-top:-10px;">&times;</button>\
						   <form class="no-margin">\
							  <label>Change event name &nbsp;</label>\
							  <input class="middle" autocomplete="off" type="text" value="' + calEvent.title + '" />\
							 <button type="submit" class="btn btn-sm btn-success"><i class="ace-icon fa fa-check"></i> Save</button>\
						   </form>\
						 </div>\
						 <div class="modal-footer">\
							<button type="button" class="btn btn-sm btn-danger" data-action="delete"><i class="ace-icon fa fa-trash-o"></i> Delete Event</button>\
							<button type="button" class="btn btn-sm" data-dismiss="modal"><i class="ace-icon fa fa-times"></i> Cancel</button>\
						 </div>\
					  </div>\
					 </div>\
					</div>';


			modal = $(modal).appendTo('body');
			modal.find('form').on('submit', function (ev) {
				ev.preventDefault();

				calEvent.title = $(this).find("input[type=text]").val();
				calendar.fullCalendar('updateEvent', calEvent);
				modal.modal("hide");
			});
			modal.find('button[data-action=delete]').on('click', function () {
				calendar.fullCalendar('removeEvents', function (ev) {
					return (ev._id == calEvent._id);
				});
				modal.modal("hide");
			});

			modal.modal('show').on('hidden', function () {
				modal.remove();
			});
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
							start: new Date(parseInt(s_datetime[0]), parseInt(s_datetime[1])-1, parseInt(s_datetime[2]), parseInt(s_datetime[3]), parseInt(s_datetime[4])),
							end: new Date(parseInt(e_datetime[0]), parseInt(e_datetime[1])-1, parseInt(e_datetime[2]), parseInt(e_datetime[3]), parseInt(e_datetime[5])),
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


