list(1)
/*
 * list terminal
 */
function list(page) {
	var url = "/terminal/list";
	var data = {
		"search_code" : $("#search_code").val(),
		"search_meeting_name" : $("#search_meeting_name").val(),
		"page" : page
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
 * uncheck other terminal
 */
function checkterminal(self) {
	var boxes = $("input[name='idbox']");
	$.each(boxes, function(index, box) {
		if (box != self) {
			box.checked = false;
		}
	});
}
/*
 * to add terminal
 */
function to_add() {
	var url = "/terminal/to_add";
	$("#modalWrapper").load(url, {}, function(response, status) {
		if (status == "error") {
			redirect_to("/");
		} else {
			$("#addModal").modal();
		}

	});
}
/*
 * add terminal
 */
function add() {
    var pad_code = $.trim($("#pad_code").val());
	var room_id = $.trim($("#room_id").val());
	if (pad_code == '') {
		$('#pad_code').focus();
		$('#terminal_cue').html("<font color='red'>终端编码不能为空</font>");
		return false;
	}
	if (is_str_unsafe(pad_code) == true) {
		$('#pad_code').focus();
		$('#terminal_cue').html("<font color='red'>终端编码含有非法字符</font>");
		return false;
	}
	if (is_str_toolong(pad_code) == true) {
		$('#pad_code').focus();
		$('#terminal_cue').html("<font color='red'>终端编码超过最大长度</font>");
		return false;
	}
	$.ajax({
		type : "POST",
		url : "/terminal/add",
		data : {
			"pad_code" : pad_code,
			"room_id" : room_id
		},
		error : function() {
			$.messager.popup("新增终端失败");
		},
		success : function(data) {
			if (data.success == "true") {
				$("#addModal").modal('hide');
				$.messager.popup("新增终端成功！");
				list(1)
			}
			else{
				$.messager.popup("新增终端失败，请检查相关信息后重试！");
			}
		},
	})
}
/*
 * to update terminal
 */
function to_update() {
	var idbox = $("input[name='idbox']:checked");
	if (idbox.length > 0) {
		var url = "/terminal/to_update";
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
		$.messager.popup("请先选择一个终端");
	}
}
/*
 * update terminal
 */
function update() {
	var id = $("#terminal_id").val()
	var pad_code = $.trim($("#pad_code").val());
	var room_id = $.trim($("#room_id").val());
	if (pad_code == '') {
		$('#pad_code').focus();
		$('#terminal_cue').html("<font color='red'>终端编码不能为空</font>");
		return false;
	}
	if (is_str_unsafe(pad_code) == true) {
		$('#pad_code').focus();
		$('#terminal_cue').html("<font color='red'>终端编码含有非法字符</font>");
		return false;
	}
	if (is_str_toolong(pad_code) == true) {
		$('#pad_code').focus();
		$('#terminal_cue').html("<font color='red'>终端编码超过最大长度</font>");
		return false;
	}
	$.ajax({
		type : "POST",
		url : "/terminal/update",
		data : {
			"id" : id,
			"pad_code" : pad_code,
			"room_id" : room_id
		},
		error : function() {
			$.messager.popup("更新终端失败");
		},
		success : function(data) {
			if (data.success) {
				$("#addModal").modal('hide');
				$.messager.popup("更新终端成功！");
				list(1)
			}
		},
	})
}
/*
 * delete terminal
 */
function del() {
	var idbox = $("input[name='idbox']:checked");
	if (idbox.length > 0) {
		$.messager.model = { 
		        ok:{ text: "确定" },
		        cancel: { text: "取消"}
		      };
		$.messager.confirm("提示", "你确定要删除该终端吗？", function() { 
			$.ajax({
				type : "POST",
				url : "/terminal/del",
				data : {
					"id" : idbox.val()
				},
				error : function() {
					$.messager.popup("删除终端失败");
				},
				success : function(data) {
					if (data.success) {
						$.messager.popup("删除终端成功！");
						list(1)
					}
				},
			})
	      });
	} else {
		$.messager.popup("请先选择一个终端");
	}
}
