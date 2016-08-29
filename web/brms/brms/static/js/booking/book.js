/**
 * Created by xyy on 2016/8/29.
 */
init();
Date.prototype.Format = function(fmt)
{ //author: meizz
  var o = {
    'M+' : this.getUTCMonth()+1,                 //月份
    'd+' : this.getUTCDate(),                    //日
    'h+' : this.getUTCHours(),                   //小时
    'm+' : this.getUTCMinutes(),                 //分
    'q+' : Math.floor((this.getUTCMonth()+3)/3) //季度
  };
  if(/(y+)/.test(fmt))
    fmt=fmt.replace(RegExp.$1, (this.getUTCFullYear()+'').substr(4 - RegExp.$1.length));
  for(var k in o)
    if(new RegExp('('+ k +')').test(fmt))
	  fmt = fmt.replace(RegExp.$1, (RegExp.$1.length==1) ? (o[k]) : (('00'+ o[k]).substr((''+ o[k]).length)));
  return fmt;
};
Date.prototype.FormatLocal = function(fmt)
{ //author: meizz
  var o = {
    'M+' : this.getMonth()+1,                 //月份
    'd+' : this.getDate(),                    //日
    'h+' : this.getHours(),                   //小时
    'm+' : this.getMinutes(),                 //分
    'q+' : Math.floor((this.getMonth()+3)/3) //季度
  };
  if(/(y+)/.test(fmt))
    fmt=fmt.replace(RegExp.$1, (this.getFullYear()+'').substr(4 - RegExp.$1.length));
  for(var k in o)
    if(new RegExp('('+ k +')').test(fmt))
	  fmt = fmt.replace(RegExp.$1, (RegExp.$1.length==1) ? (o[k]) : (('00'+ o[k]).substr((''+ o[k]).length)));
  return fmt;
};

function init() {
	scheduler.locale.labels.timeline_tab = "Timeline";
	scheduler.locale.labels.section_custom="Section";
	scheduler.config.details_on_create=true;
	scheduler.config.details_on_dblclick=true;
	scheduler.config.xml_date="%Y-%m-%d %H:%i";

	//===============
	//Configuration
	//===============

	var elements = [ // original hierarhical array to display
		{key:10, label:"Web Testing Dep.", open: true, children: [
			{key:20, label:"Elizabeth Taylor"},
			{key:30, label:"Managers",  children: [
				{key:40, label:"John Williams"},
				{key:50, label:"David Miller"},
				{key:100, label:"xyy"}
			]},
			{key:60, label:"Linda Brown"},
			{key:70, label:"George Lucas"}
		]},
		{key:110, label:"Human Relations Dep.", open:true, children: [
			{key:80, label:"Kate Moss"},
			{key:90, label:"Dian Fossey"}
		]}
	];

	scheduler.createTimelineView({
		section_autoheight: false,
		name:	"timeline",
		x_unit:	"minute",
		x_date:	"%H:%i",
		x_step:	30,
		x_size: 24,
		x_start: 16,
		x_length:	48,
		y_unit: elements,
		y_property:	"section_id",
		render: "tree",
		folder_dy:20,
		dy:60
	});

	//===============
	//Data loading
	//===============
	scheduler.config.lightbox.sections=[
		{ name:"会议名称", height:130, map_to:"text", type:"textarea" , focus:true},
		{ name:"会议描述", height:130, map_to:"desc", type:"textarea" , focus:true},
		{ name:"custom", height:23, type:"timeline", options:null , map_to:"section_id" }, //type should be the same as name of the tab
		{ name: "recurring", type: "recurring", map_to: "", button: "recurring"},
		{ name:"time", height:72, type:"calendar_time", map_to:"auto"}
	]

	scheduler.init('scheduler_here',new Date(),"timeline");
	scheduler.parse([
		{ start_date: "2016-08-29 09:00", end_date: "2016-08-29 12:00", text:"Task A-12458", section_id:20, id:11},
		{ start_date: "2016-08-29 10:00", end_date: "2016-08-29 16:00", text:"Task A-89411", section_id:20, id:12},
		{ start_date: "2016-08-29 10:00", end_date: "2016-08-29 14:00", text:"Task A-64168", section_id:20, id:13},
		{ start_date: "2016-08-29 16:00", end_date: "2016-08-29 17:00", text:"Task A-46598", section_id:20, id:14},

		{ start_date: "2016-08-29 12:00", end_date: "2016-08-29 20:00", text:"Task B-48865", section_id:40, id:15},
		{ start_date: "2016-08-29 14:00", end_date: "2016-08-29 16:00", text:"Task B-44864", section_id:40, id:16},
		{ start_date: "2016-08-29 16:30", end_date: "2016-08-29 18:00", text:"Task B-46558", section_id:40, id:17},
		{ start_date: "2016-08-29 18:30", end_date: "2016-08-29 20:00", text:"Task B-45564", section_id:40, id:18},

		{ start_date: "2016-08-29 08:00", end_date: "2016-08-29 12:00", text:"Task C-32421", section_id:50, id:19},
		{ start_date: "2016-08-29 14:30", end_date: "2016-08-29 16:45", text:"Task C-14244", section_id:50, id:10},

		{ start_date: "2016-08-29 09:20", end_date: "2016-08-29 12:20", text:"Task D-52688", section_id:60, id:20},
		{ start_date: "2016-08-29 11:40", end_date: "2016-08-29 16:30", text:"Task D-46588", section_id:60, id:21},
		{ start_date: "2016-08-29 12:00", end_date: "2016-08-29 18:00", text:"Task D-12458", section_id:60, id:22}
	],"json");
	scheduler.attachEvent("onEventChanged", function(id,ev){
		var parms = {pid:id,event:ev.text,startDate:ev.start_date,endDate:ev.end_date};
		var name = $.trim(ev.text);
		var desc = $.trim(ev.text);
		var room_id = $.trim(ev.section_id);
		var start = new Date(ev.start_date).FormatLocal('yyyy-MM-dd hh:mm');
		alert(start);
		var start_date = start.substring(0,10);
		var start_time = start.substring(11,16);
		var end = new Date(ev.end_date).pattern('yyyy-MM-dd hh:mm');
		var end_date = end.substring(0,10);
		var end_time = end.substring(11,16);
		alert("id:"+id);
		alert("event:"+ev.text);
		alert("startDate:"+start_date);
		alert("endDate:"+end_date);
		$.post("/meeting/add",parms,function(data,status){
			if(data.result=="SUCCESS"){
				if (data.success) {
					$.messager.popup("新增会议成功！");
				}else{
					var msg = data.error_msg
					$.messager.popup(msg);
				}
			}
		});
		return true;
		});

}