
function zTreeOnCheck4MB(event, treeId, treeNode) {
    var names = get_orgs("names");
    $('#search_org_name').val(names);
    load_br();
    load_meeting();
}

function load_br() {
    var org_ids = get_orgs("org_ids");
    if (org_ids.length == 0) {
        document.getElementById('room_id').innerHTML = '';
        var opt = document.createElement('option');
        opt.innerText = '--请选择会议室--';
        opt.value = '';
        opt.selected = 'selected';
        $('#room_id').append(opt);
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
                document.getElementById('room_id').innerHTML = '';
                var all = document.createElement('option');
                all.innerText = '该机构下所有会议室';
                all.value = 0;
                all.selected = 'selected';
                $('#room_id').append(all);
                for (var index = 0; index < data.brs.length; index++) {
                    opt = document.createElement('option');
                    opt.innerText = data.brs[index]['br_name'];
                    opt.value = data.brs[index]['br_id'];
                    $('#room_id').append(opt);
                }

            } else {
                $.messager.popup(data.error_msg);
            }
        }
    });
}

function load_meeting(){
    try{
        scheduler.destroy();
    }catch(e){}
    init();
}

function init() {
    scheduler.locale.labels.timeline_tab = "Timeline";
    scheduler.locale.labels.section_custom = "Section";
    scheduler.config.details_on_create = true;
    scheduler.config.details_on_dblclick = true;
    scheduler.config.xml_date = "%Y-%m-%d %H:%i";
    scheduler.config.first_hour = 7;
    scheduler.config.last_hour = 21;
    scheduler.config.time_step = 30;
    scheduler.config.readonly_form = true;

    var org_ids = get_orgs("org_ids");
    var room_id = $.trim($('#room_id').val());
    var elements;
    $.ajax({
        type: "POST",
        async: false,
        url: '/booking/org_room_list',
        data: {
            "org_ids": JSON.stringify(org_ids),
            "room_id": room_id
        },
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
            alert('机构会议室数据错误！');
        }
    });

    scheduler.config.lightbox.sections = [
        {name: "会议名称", height: 130, map_to: "text", type: "textarea", focus: true},
        {name: "会议描述", height: 130, map_to: "desc", type: "textarea", focus: true},
        {name: "会议室", height: 23, type: "timeline", options: null, map_to: "room_id"},
        {name: "recurring", type: "recurring", map_to: "", button: "recurring"},
        {name: "time", height: 72, type: "calendar_time", map_to: "auto"}
    ];
    scheduler.init('scheduler_here', new Date(), "timeline");
    $.ajax({
        type: "POST",
        async: false,
        url: '/booking/list_by_br',
        data: {
            "org_ids": JSON.stringify(org_ids),
            "room_id": room_id
        },
        success: function (data) {
            var meetings = data.meetings;
            scheduler.parse(meetings, "json");
        },
        error: function () {
            alert('会议数据错误！');
        }
    });
    // scheduler.attachEvent("onEventSave", function(id, ev){
    //     alert('111'+d);
    //
    // });
    // scheduler.attachEvent("onEventAdded", function(id, ev){
    //     alert('222'+d);
    //
    // });
    // scheduler.attachEvent("onDblClick", function(id, ev){
    //     alert(id);
    // });
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
                    var msg = data.error_msg;
                    $.messager.popup(msg);
                }
            }
        });
        return true;
    });

}

function get_orgs(type){
    var treeObj = $.fn.zTree.getZTreeObj("treeDemo");
    var nodes = treeObj.getCheckedNodes(true);
    var i=0;
    if (type == "names"){
        var org_names = "";
        for(i=0;i<nodes.length;i++){
            org_names += nodes[i].name + ",";
        }
        return org_names;
    }
    if (type == "org_ids"){
        var org_ids = [];
        for(i=0;i<nodes.length;i++){
            org_ids.push(nodes[i].id);
        }
        return org_ids;
    }

}

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
