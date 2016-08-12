list(1);
/*
 * list meeting
 */
function list(page) {
	var url = "/meeting/list";
	var data = {
		"name" : $("#search").val(),
		"page" : page,
	}
	$("#listWrapper").load(url, data, function(response, status) {
		if (status == 'error') {
			redirect_to("/");
		}
	});
}
/*
 * find a page
 */
function page() {
	var pageNo = $("#pageNo").val()
	if (isNaN(pageNo)){
		$.messager.popup('错误的页码，请重新输入')
		return false
	}
	list(pageNo)
}
/*
 * uncheck other meeting
 */
function checkmeeting(self) {
	var boxes = $("input[name='idbox']")
	$.each(boxes, function(index, box) {
		if (box != self) {
			box.checked = false;
		}
	});
}
/*
 * to add meeting
 */
function to_add() {
	var url = "/meeting/to_add";
	$("#modalWrapper").load(url, {}, function(response, status) {
		if (status == "error") {
			redirect_to("/");
		} else {
			$("#addModal").modal();
		}
	});
}
/*
 * add meeting
 */
function add() {
	var name = $.trim($("#name").val());
	var desc = $.trim($("#desc").val());
	var start = $("#start_date").val();
	var start_date = start.substring(0,10);
	var start_time = start.substring(11,16);
	var end = $("#end_date").val();
	var end_date = end.substring(0,10);
	var end_time = end.substring(11,16);
	if (name == '') {
		$('#name').focus();
		$('#meeting_cue').html("<font color='red'>会议主题不能为空</font>");
		return false;
	}
	if (is_str_unsafe(name) == true) {
		$('#name').focus();
		$('#meeting_cue').html("<font color='red'>会议主题含有非法字符</font>");
		return false;
	}
	if (is_str_toolong(name) == true) {
		$('#name').focus();
		$('#meeting_cue').html("<font color='red'>会议主题超过最大长度</font>");
		return false;
	}
	if (desc == '') {
		$('#desc').focus();
		$('#meeting_cue').html("<font color='red'>滚动文字不能为空</font>");
		return false;
	}
	if (is_str_unsafe(desc) == true) {
		$('#desc').focus();
		$('#meeting_cue').html("<font color='red'>滚动文字含有非法字符</font>");
		return false;
	}
	if (is_str_toolong(desc, 100) == true) {
		$('#desc').focus();
		$('#meeting_cue').html("<font color='red'>滚动文字超过最大长度</font>");
		return false;
	}
	$.ajax({
		type : "POST",
		url : "/meeting/add",
		data : {
			"name" : name,
			"desc" : desc,
			"start_date" : start_date,
			"start_time" : start_time,
			"end_date" : end_date,
			"end_time" : end_time
		},
		error : function() {
			$.messager.popup("新增会议失败");
		},
		success : function(data) {
			if (data.success == "true") {
				$("#addModal").modal('hide');
				$.messager.popup("新增会议成功！");
				list(1)
			}
			else{
				$.messager.popup("新增会议失败，请检查相关信息后重试！");
			}
		},
	})
}
/*
 * to update meeting
 */
function to_update() {
	var idbox = $("input[name='idbox']:checked");
	if (idbox.length > 0) {
		var url = "/meeting/to_update";
		var data = {
			"id" : idbox.val()
		};
		$("#modalWrapper").load(url, data, function(response, status) {
			if (status == "error") {
				redirect_to("/");
			} else {
				$("#addModal").modal();
			}
		});
	} else {
		$.messager.popup("请先选择一个会议");
	}
}
/*
 * update meeting
 */
function update() {
	var id = $("#meeting_id").val()
	var name = $.trim($("#name").val());
	var desc = $.trim($("#desc").val());
	var start = $("#start_date").val();
	var start_date = start.substring(0,10);
	var start_time = start.substring(11,16);
	var end = $("#end_date").val();
	var end_date = end.substring(0,10);
	var end_time = end.substring(11,16);
	if (name == '') {
		$('#name').focus();
		$('#meeting_cue').html("<font color='red'>会议主题不能为空</font>");
		return false;
	}
	if (is_str_unsafe(name) == true) {
		$('#name').focus();
		$('#meeting_cue').html("<font color='red'>会议主题含有非法字符</font>");
		return false;
	}
	if (is_str_toolong(name) == true) {
		$('#name').focus();
		$('#meeting_cue').html("<font color='red'>会议主题超过最大长度</font>");
		return false;
	}
	if (desc == '') {
		$('#desc').focus();
		$('#meeting_cue').html("<font color='red'>滚动文字不能为空</font>");
		return false;
	}
	if (is_str_unsafe(desc) == true) {
		$('#desc').focus();
		$('#meeting_cue').html("<font color='red'>滚动文字含有非法字符</font>");
		return false;
	}
	if (is_str_toolong(desc, 100) == true) {
		$('#desc').focus();
		$('#meeting_cue').html("<font color='red'>滚动文字超过最大长度</font>");
		return false;
	}
	$.ajax({
		type : "POST",
		url : "/meeting/update",
		data : {
			"id" : id,
			"name" : name,
			"desc" : desc,
			"start_date" : start_date,
			"start_time" : start_time,
			"end_date" : end_date,
			"end_time" : end_time
		},
		error : function() {
			$.messager.popup("更新会议失败");
		},
		success : function(data) {
			if (data.success) {
				$("#addModal").modal('hide');
				$.messager.popup("更新会议成功！");
				list(1)
			}
		},
	})
}
/*
 * delete meeting
 */
function del() {
	var idbox = $("input[name='idbox']:checked");
	if (idbox.length > 0) {
		$.messager.model = { 
		        ok:{ text: "确定" },
		        cancel: { text: "取消"}
		      };
		$.messager.confirm("提示", "你确定要删除该会议吗？", function() { 
			$.ajax({
				type : "POST",
				url : "/meeting/del",
				data : {
					"id" : idbox.val()
				},
				error : function() {
					$.messager.popup("删除会议失败");
				},
				success : function(data) {
					if (data.success) {
						$.messager.popup("删除会议成功！");
						list(1)
					}
				},
			})
	      });
	} else {
		$.messager.popup("请先选择一个会议");
	}
}
