listRole(1);
listUser(1);
/*
 * list user
 */
function listUser(page) {
	var url = "/user/list";
	var data = {
		"user_account" : $("#user_account").val(),
		"user_name" : $("#user_name").val(),
		"org_id" : $("#search_org_id").val(),
		"role_name" : $("#role_name").val(),
		"page" : page
	};
	$("#listWrapperUser").load(url, data, function(response, status) {
		if (status == "error") {
			redirect_to("/");
		}
	});
}
/*
 * list role
 */
function listRole(page) {
	var url = "/role/list";
	var data = {
		"name" : $("#search").val(),
		"page" : page,
	}
	$("#listWrapperRole").load(url, data, function(response, status) {
		if (status == 'error') {
			redirect_to("/");
		}
	});
}
/*
 * find a user page
 */
function pageUser() {
	var pageNo = $("#pageNo").val();
	if (isNaN(pageNo)){
		$.messager.popup('错误的页码，请重新输入');
		return false
	}
	listUser(pageNo);
}
/*
 * find a role page
 */
function pageRole() {
	var pageNo = $("#pageRoleNo").val()
	if (isNaN(pageNo)){
		$.messager.popup('错误的页码，请重新输入')
		return false
	}
	listRole(pageNo)
}
/*
 * uncheck other role
 */
function checkrole(self) {
	var boxes = $("input[name='idbox']")
	$.each(boxes, function(index, box) {
		if (box != self) {
			box.checked = false;
		}
	});
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
 * to update role
 */
function to_auth_user() {
	var idbox = $("input[name='idbox']:checked");
	if (idbox.length > 0) {
		var url = "/auth/to_auth_user";
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
		$.messager.popup("请先选择一个用户");
	}
}
/*
 * to update role
 */
function to_auth_role() {
	var idbox = $("input[name='idbox']:checked");
	if (idbox.length > 0) {
		var url = "/auth/to_auth_role";
		var data = {
			"id" : idbox.val()
		};
		$("#modalRoleWrapper").load(url, data, function(response, status) {
			if (status == "error") {
				redirect_to("/");
			} else {
				$("#roleModal").modal();
			}
		});
	} else {
		$.messager.popup("请先选择一个用户");
	}
}
/*
 * update role
 */
function update_auth_user() {
	var user_id = $("#user_id").val();
	var treeObj=$.fn.zTree.getZTreeObj("treeUserOrg"),
	nodes=treeObj.getCheckedNodes(true),
	org_ids="",
	org_names="";
	for(var i=0;i<nodes.length;i++){
		org_names+=nodes[i].name + ",";
		org_ids+=nodes[i].id + ",";
	}
	$.ajax({
		type : "POST",
		url : "/auth/update_auth_user",
		data : {
			"user_id" : user_id,
			"org_ids" : org_ids.substr(0,org_ids.length-1)
		},
		error : function() {
			$.messager.popup("用户授权失败！");
		},
		success : function(data) {
			if (data.success) {
				$("#addModal").modal('hide');
				$.messager.popup("用户授权成功！");
				listUser(1);
			}
		},
	})
}