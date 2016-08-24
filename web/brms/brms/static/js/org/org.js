/**
 * Created by cuizc on 16-8-15.
 */
list(1);
/*
 * list org
 */
function list(page) {
	var url = "/org/list";
	var data = {
		"org_name" : $("#org_name").val(),
		"parent_id" : $("#search_org_id").val(),
		"address" : $("#address").val(),
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
 * uncheck other org
 */
function checkorg(self) {
	var boxes = $("input[name='idbox']");
	$.each(boxes, function(index, box) {
		if (box != self) {
			box.checked = false;
		}
	});
}
/*
 * to add org
 */
function to_add() {
	var url = "/org/to_add_org";
	$("#modalWrapper").load(url, {}, function(response, status) {
		if (status == "error") {
			redirect_to("/");
		} else {
			$("#addModal").modal();
		}
	});
}

/*
 * add org
 */
function add() {
	var org_name = $.trim($("#org_name_add").val());
	var parent_id = $.trim($("#parent_id_add").val());
    var org_seq = $.trim($("#org_seq_add").val());
	var org_manager = $.trim($("#org_manager_add").val());
	var phone = $.trim($('#phone_add').val());
    var address = $.trim($('#address_add').val());
    // var state = $.trim($('#state_add').val());
	if (org_name == '') {
		$('#org_name_add').focus();
		$('#org_cue').html("<font color='red'>机构名称不能为空</font>");
		return false;
	}
	if (is_str_unsafe(org_name) == true) {
		$('#org_name_add').focus();
		$('#org_cue').html("<font color='red'>机构名称含有非法字符</font>");
		return false;
	}
	if (parent_id == '') {
		// $('#parent_id_add').focus();
		// $('#org_cue').html("<font color='red'>上级机构不能为空</font>");
		// return false;
		parent_id = 0;
	}
    if (org_seq == '') {
        org_seq = 1000;
    }
	// if (state == '') {
	// 	state = 1;
	// }
	$.ajax({
		type : "POST",
		url : "/org/add_org",
		data : {
			"org_name" : org_name,
			"parent_id" : parent_id,
            "org_seq": org_seq,
			"org_manager" : org_manager,
			"phone" : phone,
			"address" : address
			// "state" : state
		},
		error : function() {
			redirect_to("/");
		},
		success : function(data) {
			if (data.resultFlag == "success") {
				$("#addModal").modal('hide');
				$.messager.popup('新增机构成功！');
				list(1)
			} else {
				$.messager.popup(data.error_msg);
			}
		}
	})
}
/*
 * to update boardroom
 */
function to_update() {
	var idbox = $("input[name='idbox']:checked");
	if (idbox.length > 0) {
		var url = "/org/to_update_org";
		var data = {
			"org_id" : idbox.val()
		};
		$("#modalWrapper").load(url, data, function(response, status) {
			if (status == "error") {
				redirect_to("/");
			} else {
				$("#addModal").modal();
			}
		});
	} else {
		$.messager.popup('请先选择一个机构！')
	}
}
/*
 * update org
 */
function update() {
    var org_id = $.trim($("#org_id").val());
    var org_name = $.trim($("#org_name_add").val());
	var parent_id = $.trim($("#parent_id_add").val());
    var org_seq = $.trim($("#org_seq_add").val());
	var org_manager = $.trim($("#org_manager_add").val());
	var phone = $.trim($('#phone_add').val());
    var address = $.trim($('#address_add').val());
    // var state = $.trim($('#state_add').val());
    if (org_id == '') {
        $.messager.popup('更新失败，请刷新页面后重试！');
        return false;
    }
	if (org_name == '') {
		$('#org_name_add').focus();
		$('#org_cue').html("<font color='red'>机构名称不能为空</font>");
		return false;
	}
	if (is_str_unsafe(org_name) == true) {
		$('#org_name_add').focus();
		$('#org_cue').html("<font color='red'>机构名称含有非法字符</font>");
		return false;
	}
	if (parent_id == '') {
		$('#parent_id_add').focus();
		$('#org_cue').html("<font color='red'>上级机构不能为空</font>");
		return false;
	}
    if (org_seq == '') {
        org_seq = 1000;
    }
	// if (state == '') {
	// 	state = 1;
	// }
	$.ajax({
		type : "POST",
		url : "/org/add_org",
		data : {
            "org_id": org_id,
			"org_name" : org_name,
			"parent_id" : parent_id,
            "org_seq": org_seq,
			"org_manager" : org_manager,
			"phone" : phone,
			"address" : address
			// "state" : state
		},
		error : function() {
			redirect_to("/");
		},
		success : function(data) {
			if (data.resultFlag == "success") {
				$("#addModal").modal('hide');
				$.messager.popup('更新机构成功！');
				list(1)
			} else {
				$.messager.popup(data.error_msg);
			}
		}
	})
}
/*
 * delete org
 */
function del() {
	var idbox = $("input[name='idbox']:checked");
	if (idbox.length > 0) {
		$.messager.model = {
		        ok:{ text: "确定" },
		        cancel: { text: "取消"}
		      };
		$.messager.confirm("提示", "你确定要删除该机构吗？", function() {
			$.ajax({
				type : "POST",
				url : "/org/delete_org",
				data : {
					"org_id" : idbox.val()
				},
				error : function() {
					redirect_to("/");
				},
				success : function(data) {
					if (data.resultFlag == "success") {
						$("#addModal").modal('hide');
						$.messager.popup('删除机构成功！');
						list(1)
					} else {
						$.messager.popup(data.error_msg);
					}
				}
			});
		});
	} else {
		$.messager.popup("请先选择一个机构！");
	}
}
