
function zTreeOnCheck4MB(event, treeId, treeNode) {
    var names = get_orgs("names");
    $('#search_org_name').val(names);
    load_br();
    refresh_calender();
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
        error: ajax_error,
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

function refresh_calender(){
    var org_ids = get_orgs("org_ids");
    if (org_ids.length == 0) {
        return ;
    }
    try{
        // scheduler.clearAll();
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
    scheduler.config.lightbox_recurring = 'series';
    scheduler.config.collision_limit = 1;
    scheduler.config.drag_in = false;
    scheduler.config.drag_move = false;
    scheduler.config.drag_resize= false;
    scheduler.config.repeat_precise = true;
    scheduler.config.event_duration = 60;
    scheduler.config.auto_end_date = true;

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
                x_step: 60,
                x_size: 14,
                x_start: 7,
                x_length: 24,
                y_unit: elements,
                y_property: "room_id",
                render: "tree",
                folder_dy: 20,
                dy: 60
            });
        },
        error: ajax_error
    });

    scheduler.init('scheduler_here', new Date(), "timeline");
    load_meetings(org_ids, room_id);
}

function reload_meeting(){
    var org_ids = get_orgs("org_ids");
    var room_id = $.trim($('#room_id').val());
    load_meetings(org_ids, room_id);
}

function load_meetings(org_ids, room_id){
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
        error: ajax_error
    });
}

function get_orgs(type){
    var treeObj = $.fn.zTree.getZTreeObj("treeDemo");
    var nodes = treeObj.getCheckedNodes(true);
    var i=0;
    if (type == "names"){
        var org_names = nodes[0].name;
        for(i=1;i<nodes.length;i++){
            org_names += "," + nodes[i].name;
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

function get_rec(rec_type, i){
    if (rec_type == ''){
        return '';
    }
    if (rec_type.indexOf('#') >= 0){
        var result = rec_type.split('#');
        return result[i];
    }
    return [rec_type, ''][i];
}

function compare_date(d1,d2)
{
    return ((new Date(d1.replace(/-/g, "\/"))) > (new Date(d2.replace(/-/g, "\/"))));
}
