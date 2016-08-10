list(1);
/*
 * list user
 */
function list(page) {
	var url = "/user/list";
	var data = {
		"user_account" : $("#user_account1").val(),
		"user_name" : $("#user_name").val(),
		"org_id" : $("#org_id").val(),
		"role_name" : $("#role_name").val(),
		"page" : page
	};
	$("#listWrapper").load(url, data, function(response, status) {
		if (status == "error") {
			redirect_to("/");
		}
	});
}

/*
 * find a page
 */
function page() {
	var pageNo = $("#pageNo").val();
	if (isNaN(pageNo)){
		$.messager.popup('错误的页码，请重新输入');
		return false
	}
	list(pageNo);
}
/*
 * uncheck other role
 */
function checkuser(self) {
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
	var url = "/user/to_add_user";
	$("#modalWrapper").load(url, {}, function(response, status) {
		if (status == "error") {
			redirect_to("/");
		} else {
			$("#addModal").modal();
		}
	});
}
/*
 * add user
 */
function add() {
	var user_account = $.trim($("#user_account_add").val());
	var user_name = $.trim($("#user_name_add").val());
	var branch = $.trim($("#branch_add").val());
	// var password = $.trim($("#password_add").val());
    var max_period = $.trim($("#max_period_add").val());
	var email = $.trim($("#email_add").val());
	var phone = $.trim($("#phone_add").val());
	var position = $.trim($("#position_add").val());
	var state = $.trim($("#state_add").val());
	if (user_account == '') {
		$('#user_account_add').focus();
		$('#user_cue').html("<font color='red'>用户帐号不能为空</font>");
		return false;
	}
	if (is_str_unsafe(user_account) == true) {
		$('#user_account_add').focus();
		$('#user_cue').html("<font color='red'>用户帐号含有非法字符</font>");
		return false;
	}
	if (is_str_toolong(user_account) == true) {
		$('#user_account_add').focus();
		$('#user_cue').html("<font color='red'>用户帐号超过最大长度</font>");
		return false;
	}
	if (user_name == '') {
		$('#user_name_add').focus();
		$('#user_cue').html("<font color='red'>用户姓名不能为空</font>");
		return false;
	}
	if (is_str_unsafe(user_name) == true) {
		$('#user_name_add').focus();
		$('#user_cue').html("<font color='red'>用户姓名含有非法字符</font>");
		return false;
	}
	if (is_str_toolong(user_name) == true) {
		$('#user_name_add').focus();
		$('#user_cue').html("<font color='red'>用户姓名超过最大长度</font>");
		return false;
	}
	if (branch == '') {
		$('#branch_add').focus();
		$('#user_cue').html("<font color='red'>用户机构不能为空</font>");
		return false;
	}
    if (max_period == '') {
        $('#max_period_add').value = 7;
        max_period = 7;
    }
    if (max_period > 30 || max_period < 1) {
        $('#max_period').focus();
        $('#user_cue').html("<font color='red'>预约期限范围为1～30天(默认为7天)</font>")
    }
	if (email == '') {
		$('#email_add').focus();
		$('#user_cue').html("<font color='red'>用户email不能为空</font>");
		return false;
	}
	var emailPat=/^([a-zA-Z0-9_-].*)+@([a-zA-Z0-9_-].*)+(.com)$/;
	var matchArray=email.match(emailPat);
	if (matchArray==null) {
		$.messager.popup('电子邮件地址格式不正确 (样例格式:xxxx@xxx.com)');
		return false;
	}
	$.ajax({
		type : "POST",
		url : "/user/add_user",
		data : {
			"user_account" : user_account,
			"user_name" : user_name,
			"org_id" : branch,
            "max_period": max_period,
			"email" : email,
			"phone" : phone,
			"position" : position,
			"state" : state
		},
		error : function() {
			redirect_to("/");
		},
		success : function(data) {
			if (data.resultFlag == "success") {
				$("#addModal").modal('hide');
				$.messager.popup('新增用户成功！密码已发送到该用户邮箱！');
				list(1)
			} else {
				$.messager.popup(data.error_msg);
			}
		}
	})
}
/*
 * to update user
 */
function to_update() {
	var idbox = $("input[name='idbox']:checked");
	if (idbox.length > 0) {
		var url = "/user/to_update_user";
		var data = {
			"user_id" : idbox.val()
		};
		$("#modalWrapper").load(url, data, function(response, status) {
			if (status == "error") {
				redirect_to("/");
			} else {
				$("#addModal").modal();
			}
		});
	} else {
		$.messager.popup('请先选择一个用户！')
	}
}
/*
 * update user
 */
function update() {
    var user_id = $.trim($("#user_id").val());
	var user_account = $.trim($("#user_account_add").val());
	var user_name = $.trim($("#user_name_add").val());
	var branch = $.trim($("#branch_add").val());
	// var password = $.trim($("#password_add").val());
    var max_period = $.trim($("#max_period_add").val());
	var email = $.trim($("#email_add").val());
	var phone = $.trim($("#phone_add").val());
	var position = $.trim($("#position_add").val());
	var state = $.trim($("#state_add").val());
    if (user_id == '') {
        $('#user_cue').html("<font color='red'>用户ID为空,请刷新页面重试</font>");
        return false;
    }
	if (user_account == '') {
		$('#user_account_add').focus();
		$('#user_cue').html("<font color='red'>用户帐号不能为空</font>");
		return false;
	}
	if (is_str_unsafe(user_account) == true) {
		$('#user_account_add').focus();
		$('#user_cue').html("<font color='red'>用户帐号含有非法字符</font>");
		return false;
	}
	if (is_str_toolong(user_account) == true) {
		$('#user_account_add').focus();
		$('#user_cue').html("<font color='red'>用户帐号超过最大长度</font>");
		return false;
	}
	if (user_name == '') {
		$('#user_name_add').focus();
		$('#user_cue').html("<font color='red'>用户姓名不能为空</font>");
		return false;
	}
	if (is_str_unsafe(user_name) == true) {
		$('#user_name_add').focus();
		$('#user_cue').html("<font color='red'>用户姓名含有非法字符</font>");
		return false;
	}
	if (is_str_toolong(user_name) == true) {
		$('#user_name_add').focus();
		$('#user_cue').html("<font color='red'>用户姓名超过最大长度</font>");
		return false;
	}
	if (branch == '') {
		$('#branch_add').focus();
		$('#user_cue').html("<font color='red'>用户机构不能为空</font>");
		return false;
	}
    if (max_period == '') {
        $('#max_period_add').value = 7;
        max_period = 7;
    }
    if (max_period > 30 || max_period < 1) {
        $('#max_period').focus();
        $('#user_cue').html("<font color='red'>预约期限范围为1～30天(默认为7天)</font>")
    }
	if (email == '') {
		$('#email_add').focus();
		$('#user_cue').html("<font color='red'>用户email不能为空</font>");
		return false;
	}
	var emailPat=/^([a-zA-Z0-9_-].*)+@([a-zA-Z0-9_-].*)+(.com)$/;
	var matchArray=email.match(emailPat);
	if (matchArray==null) {
		$.messager.popup('电子邮件地址格式不正确 (样例格式:xxxx@xxx.com)');
		return false;
	}
	$.ajax({
		type : "POST",
		url : "/user/update_user",
		data : {
            "user_id": user_id,
			"user_account" : user_account,
			"user_name" : user_name,
			"org_id" : branch,
            "max_period": max_period,
			"email" : email,
			"phone" : phone,
			"position" : position,
			"state" : state
		},
		error : function() {
			redirect_to("/");
		},
		success : function(data) {
			if (data.resultFlag == "success") {
				$("#addModal").modal('hide');
				$.messager.popup('更新用户成功！');
				list(1)
			} else {
				$.messager.popup('更新用户失败');
			}
		}
	})
}
/*
 * delete user
 */
function del() {
	var idbox = $("input[name='idbox']:checked");
	if (idbox.length > 0) {
		$.messager.model = { 
		        ok:{ text: "确定" },
		        cancel: { text: "取消"}
		      };
		$.messager.confirm("提示", "你确定要删除该用户吗？", function() {
			$.ajax({
				type : "POST",
				url : "/user/delete_user",
				data : {
					"id" : idbox.val()
				},
				error : function() {
					redirect_to("/");
				},
				success : function(data) {
					if (data.success) {
						$.messager.popup("用户删除成功！");
						list(1)
					}
				}
			});
		});
	} else {
		$.messager.popup("请先选择一个用户！");
	}
}
