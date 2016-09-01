/**
 * Created by xyy on 2016/8/29.
 */
init();
Date.prototype.Format = function (fmt) {
    var o = {
        'M+': this.getUTCMonth() + 1,                 //月份
        'd+': this.getUTCDate(),                    //日
        'h+': this.getUTCHours(),                   //小时
        'm+': this.getUTCMinutes(),                 //分
        'q+': Math.floor((this.getUTCMonth() + 3) / 3) //季度
    };
    if (/(y+)/.test(fmt))
        fmt = fmt.replace(RegExp.$1, (this.getUTCFullYear() + '').substr(4 - RegExp.$1.length));
    for (var k in o)
        if (new RegExp('(' + k + ')').test(fmt))
            fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (('00' + o[k]).substr(('' + o[k]).length)));
    return fmt;
};
Date.prototype.FormatLocal = function (fmt) {
    var o = {
        'M+': this.getMonth() + 1,                 //月份
        'd+': this.getDate(),                    //日
        'h+': this.getHours(),                   //小时
        'm+': this.getMinutes(),                 //分
        'q+': Math.floor((this.getMonth() + 3) / 3) //季度
    };
    if (/(y+)/.test(fmt))
        fmt = fmt.replace(RegExp.$1, (this.getFullYear() + '').substr(4 - RegExp.$1.length));
    for (var k in o)
        if (new RegExp('(' + k + ')').test(fmt))
            fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (('00' + o[k]).substr(('' + o[k]).length)));
    return fmt;
};

function init() {
    scheduler.locale.labels.timeline_tab = "Timeline";
    scheduler.locale.labels.section_custom = "Section";
    scheduler.config.details_on_create = true;
    scheduler.config.details_on_dblclick = true;
    scheduler.config.xml_date = "%Y-%m-%d %H:%i";
    scheduler.config.first_hour = 7;
    scheduler.config.last_hour = 21;
    scheduler.config.time_step = 30;

    var elements;
    $.ajax({
        type: "POST",
        async: false,
        url: '/booking/org_room_list',
        success: function (data) {
            elements = data.org_room;
            scheduler.createTimelineView({
                section_autoheight: false,
                name: "timeline",
                x_unit: "minute",
                x_date: "%H:%i",
                x_step: 30,
                x_size: 28,
                x_start: 14,
                x_length: 48,
                y_unit: elements,
                y_property: "room_id",
                render: "tree",
                folder_dy: 20,
                dy: 60
            });
        },
        error: function () {
            alert('数据错误！');
        }
    });

    scheduler.config.lightbox.sections = [
        {name: "会议名称", height: 130, map_to: "text", type: "textarea", focus: true},
        {name: "会议描述", height: 130, map_to: "desc", type: "textarea", focus: true},
        {name: "会议室", height: 23, type: "timeline", options: null, map_to: "room_id"}, //type should be the same as name of the tab
        {name: "recurring", type: "recurring", map_to: "", button: "recurring"},
        {name: "time", height: 72, type: "calendar_time", map_to: "auto"}
    ];
    scheduler.init('scheduler_here', new Date(2016, 7, 31), "timeline");
    $.ajax({
        type: "POST",
        async: false,
        url: '/booking/list_by_br_new',
        success: function (data) {
            var meetings = data.meetings;
            scheduler.parse(meetings, "json");
        },
        error: function () {
            alert('数据错误！');
        }
    });
    scheduler.attachEvent("onEventChanged", function (id, ev) {
        debugger;
        var parms = {pid: id, event: ev.text, startDate: ev.start_date, endDate: ev.end_date};
        var name = $.trim(ev.text);
        var desc = $.trim(ev.text);
        var room_id = $.trim(ev.section_id);
        var start = new Date(ev.start_date).FormatLocal('yyyy-MM-dd hh:mm');
        var start_date = start.substring(0, 10);
        var start_time = start.substring(11, 16);
        var end = new Date(ev.end_date).pattern('yyyy-MM-dd hh:mm');
        var end_date = end.substring(0, 10);
        var end_time = end.substring(11, 16);
        $.post("/meeting/add", parms, function (data, status) {
            if (data.result == "SUCCESS") {
                if (data.success) {
                    $.messager.popup("新增会议成功！");
                } else {
                    var msg = data.error_msg
                    $.messager.popup(msg);
                }
            }
        });
        return true;
    });

}

function get_date_time(date_str, time_str) {
    date_list = date_str.concat(" " + time_str);
    return date_list;
}

function load_br(org_ids) {
    if (org_ids.length == 0) {
        document.getElementById('br_id').innerHTML = '';
        var opt = document.createElement('option');
        opt.innerText = '--请选择会议室--';
        opt.value = '';
        opt.selected = 'selected';
        $('#br_id').append(opt);
        return ;
    }
    $.ajax({
        type: 'POST',
        async : false,
        cache : false,
        url: '/booking/list_by_org',
        dataType: "json",
        data: {"org_ids": JSON.stringify(org_ids)},
        error: function () {
            $.messager.popup('与服务器通信失败，请稍后重试！');
        },
        success: function (data) {
            if (data.resultFlag == 'success') {
                document.getElementById('br_id').innerHTML = '';
                var opt = document.createElement('option');
                opt.innerText = '--请选择会议室--';
                opt.value = '';
                opt.selected = 'selected';
                $('#br_id').append(opt);
                var all = document.createElement('option');
                all.innerText = '该机构下所有会议室';
                all.value = 0;
                $('#br_id').append(all);
                for (var index = 0; index < data.brs.length; index++) {
                    opt = document.createElement('option');
                    opt.innerText = data.brs[index]['br_name'];
                    opt.value = data.brs[index]['br_id'];
                    $('#br_id').append(opt);
                }
            } else {
                $.messager.popup(data.error_msg);
            }
        }
    });
}

function zTreeOnCheck4MB(event, treeId, treeNode) {
    var treeObj=$.fn.zTree.getZTreeObj("treeDemo"),
	nodes=treeObj.getCheckedNodes(true),
	org_ids = [],
	org_names="";
	for(var i=0;i<nodes.length;i++){
		org_names += nodes[i].name + ",";
        org_ids.push(nodes[i].id);
	}
    $('#search_org_name').val(org_names);
	load_br(org_ids);
}


