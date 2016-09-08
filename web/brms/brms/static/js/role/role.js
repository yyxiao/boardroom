listRole(1);
/*
 * list role
 */
function listRole(page) {
	var url = "/role/list";
	var data = {
		"name" : $("#search").val(),
		"page" : page
	};
	$("#listWrapper").load(url, data, function(response, status) {
		if (status == 'error') {
			redirect_to("/");
		}
	});
}
/*
 * find a page
 */
function pageRole() {
	var pageNo = $("#pageRoleNo").val();
	if (isNaN(pageNo) || pageNo == ''){
		$.messager.popup('错误的页码，请重新输入');
		return false
	}
	listRole(pageNo)
}
/*
 * uncheck other role
 */
function checkrole(self) {
	var boxes = $("input[name='idbox']");
	$.each(boxes, function(index, box) {
		if (box != self) {
			box.checked = false;
		}
	});
}
/*
 * to add role
 */
function to_add() {
	var url = "/role/to_add";
	$("#modalWrapper").load(url, {}, function(response, status) {
		if (status == "error") {
			redirect_to("/");
		} else {
			$("#addModal").modal();
		}

	});
}
/*
 * add role
 */
function add() {
	var name = $.trim($("#name").val());
	var desc = $.trim($("#desc").val());
	if (name == '') {
		$('#name').focus();
		$('#role_cue').html("<font color='red'>角色名称不能为空</font>");
		return false;
	}
	if (is_str_unsafe(name) == true) {
		$('#name').focus();
		$('#role_cue').html("<font color='red'>角色名称含有非法字符</font>");
		return false;
	}
	if (is_str_toolong(name) == true) {
		$('#name').focus();
		$('#role_cue').html("<font color='red'>角色名称超过最大长度</font>");
		return false;
	}
	if (desc != '' && is_str_unsafe(desc) == true) {
		$('#desc').focus();
		$('#role_cue').html("<font color='red'>角色描述含有非法字符</font>");
		return false;
	}
	if (desc != '' && is_str_toolong(desc, 100) == true) {
		$('#desc').focus();
		$('#role_cue').html("<font color='red'>角色描述超过最大长度</font>");
		return false;
	}
	$.ajax({
		type : "POST",
		url : "/role/add",
		data : {
			"name" : name,
			"desc" : desc
		},
		error : ajax_error,
		success : function(data) {
			if (data.success == "true") {
				$("#addModal").modal('hide');
				$.messager.popup("新增角色成功！");
				listRole(1)
			}
			else{
				$.messager.popup("新增角色失败，请检查相关信息后重试！");
			}
		}
	})
}
/*
 * to update role
 */
function to_update() {
	var idbox = $("input[name='idbox']:checked");
	if (idbox.length > 0) {
		var url = "/role/to_update";
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
		$.messager.popup("请先选择一个角色");
	}
}
/*
 * update role
 */
function update() {
	var id = $("#role_id").val()
	var name = $.trim($("#name").val());
	var desc = $.trim($("#desc").val());
	if (name == '') {
		$('#name').focus();
		$('#role_cue').html("<font color='red'>角色名称不能为空</font>");
		return false;
	}
	if (is_str_unsafe(name) == true) {
		$('#name').focus();
		$('#role_cue').html("<font color='red'>角色名称含有非法字符</font>");
		return false;
	}
	if (is_str_toolong(name) == true) {
		$('#name').focus();
		$('#role_cue').html("<font color='red'>角色名称超过最大长度</font>");
		return false;
	}
	if (desc != '' && is_str_unsafe(desc) == true) {
		$('#desc').focus();
		$('#role_cue').html("<font color='red'>角色描述含有非法字符</font>");
		return false;
	}
	if (desc != '' && is_str_toolong(desc, 100) == true) {
		$('#desc').focus();
		$('#role_cue').html("<font color='red'>角色描述超过最大长度</font>");
		return false;
	}
	$.ajax({
		type : "POST",
		url : "/role/update",
		data : {
			"id" : id,
			"name" : name,
			"desc" : desc
		},
		error : ajax_error,
		success : function(data) {
			if (data.success) {
				$("#addModal").modal('hide');
				$.messager.popup("更新角色成功！");
				listRole(1)
			}
		}
	})
}
/*
 * delete role
 */
function del() {
	var idbox = $("input[name='idbox']:checked");
	if (idbox.length > 0) {
		$.messager.model = { 
		        ok:{ text: "确定" },
		        cancel: { text: "取消"}
		      };
		$.messager.confirm("提示", "你确定要删除该角色吗？", function() { 
			$.ajax({
				type : "POST",
				url : "/role/del",
				data : {
					"id" : idbox.val()
				},
				error : ajax_error,
				success : function(data) {
					if (data.success) {
						$.messager.popup("删除角色成功！");
						listRole(1)
					}
				}
			})
	      });
	} else {
		$.messager.popup("请先选择一个角色");
	}
}
