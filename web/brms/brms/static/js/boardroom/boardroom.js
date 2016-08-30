list(1);
/*
 * list boardroom
 */
function list(page) {
	var url = "/boardroom/list";
	var show_child = $("#show_child").is(":checked");
	var data = {
		"br_name" : $("#br_name").val(),
		"br_config" : $("#br_config").val(),
		"org_id" : $("#search_org_id").val(),
		"show_child": show_child,
		"flag" : $("#flag").val(),
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
 * uncheck other boardroom
 */
function checkbr(self) {
	var boxes = $("input[name='idbox']");
	$.each(boxes, function(index, box) {
		if (box != self) {
			box.checked = false;
		}
	});
}
/*
 * to add boardroom
 */
function to_add() {
	var url = "/boardroom/to_add_boardroom";
	$("#modalWrapper").load(url, {}, function(response, status) {
		if (status == "error") {
			redirect_to("/");
		} else {
			$("#addModal").modal();
		}
	});
}

//upload picture
function upload() {
	var formData = new FormData();
	formData.append('br_pic', $('#br_pic_add')[0].files[0]);
	$.ajax({
		type : "POST",
		url : "/boardroom/br_upload_pic",
		data : formData,
		async: false,
        cache: false,
        contentType: false,
        processData: false,
		success : function(data) {
			if (data.resultFlag == "success") {
				 $("#preview").html('<img src="static/img/boardroom/tmp/'+data.name+'" height="150" width="150"/>');
			} else {
				$("#preview").html(data.error_msg);
			}
		}
	});
}
/*
 * add boardroom
 */
function add() {
	// var br_id = $.trim($("#br_id").val());
	var br_name = $.trim($("#br_name_add").val());
	var branch = $.trim($("#branch_add").val());
    var br_config = $.trim($("#br_config_add").val());
	var br_desc = $.trim($("#br_desc_add").val());
	var file_path = $.trim($('#br_pic_add').val());
	if (file_path != '') {
		var br_pic = file_path.substring(file_path.lastIndexOf('\\')+1 );
	}
	// var state = $.trim($("#state_add").val());
	if (br_name == '') {
		$('#br_name_add').focus();
		$('#br_cue').html("<font color='red'>会议室名称不能为空</font>");
		return false;
	}
	if (is_str_unsafe(br_name) == true) {
		$('#br_name_add').focus();
		$('#br_cue').html("<font color='red'>会议室名称含有非法字符</font>");
		return false;
	}
	if (branch == '') {
		$('#branch_add').focus();
		$('#br_cue').html("<font color='red'>用户机构不能为空</font>");
		return false;
	}
	// if (state == '') {
	// 	state = 1;
	// }
	$.ajax({
		type : "POST",
		url : "/boardroom/add_boardroom",
		data : {
			// "br_id" : br_id,
			"br_name" : br_name,
			"org_id" : branch,
            "br_config": br_config,
			"br_desc" : br_desc,
			"br_pic" : br_pic
			// "state" : state
		},
		error : function() {
			redirect_to("/");
		},
		success : function(data) {
			if (data.resultFlag == "success") {
				$("#addModal").modal('hide');
				$.messager.popup('新增会议室成功！');
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
		var url = "/boardroom/to_update_boardroom";
		var data = {
			"br_id" : idbox.val()
		};
		$("#modalWrapper").load(url, data, function(response, status) {
			if (status == "error") {
				redirect_to("/");
			} else {
				$("#addModal").modal();
			}
		});
	} else {
		$.messager.popup('请先选择一个会议室！')
	}
}
/*
 * update boardroom
 */
function update() {
    var br_id = $.trim($("#br_id").val());
	var br_name = $.trim($("#br_name_add").val());
	var branch = $.trim($("#branch_add").val());
    var br_config = $.trim($("#br_config_add").val());
	var br_desc = $.trim($("#br_desc_add").val());
	var file_path = $.trim($('#br_pic_add').val());
	if (file_path != '') {
		var br_pic = file_path.substring(file_path.lastIndexOf('\\')+1 );
	}
	// var state = $.trim($("#state_add").val());
	if (br_id == '') {
        $('#user_cue').html("<font color='red'>更新失败,请刷新页面重试</font>");
        return false;
    }
	if (br_name == '') {
		$('#br_name_add').focus();
		$('#br_cue').html("<font color='red'>会议室名称不能为空</font>");
		return false;
	}
	if (is_str_unsafe(br_name) == true) {
		$('#br_name_add').focus();
		$('#br_cue').html("<font color='red'>会议室名称含有非法字符</font>");
		return false;
	}
	if (branch == '') {
		$('#branch_add').focus();
		$('#br_cue').html("<font color='red'>用户机构不能为空</font>");
		return false;
	}
	$.ajax({
		type : "POST",
		url : "/boardroom/update_boardroom",
		data : {
			"br_id" : br_id,
			"br_name" : br_name,
			"org_id" : branch,
            "br_config": br_config,
			"br_desc" : br_desc,
			"br_pic" : br_pic
			// "state" : state
		},
		error : function() {
			redirect_to("/");
		},
		success : function(data) {
			if (data.resultFlag == "success") {
				$("#addModal").modal('hide');
				$.messager.popup('更新会议室成功！');
				list(1)
			} else {
				$.messager.popup(data.error_msg);
			}
		}
	})
}
/*
 * delete boardroom
 */
function del() {
	var idbox = $("input[name='idbox']:checked");
	if (idbox.length > 0) {
		$.messager.model = { 
		        ok:{ text: "确定" },
		        cancel: { text: "取消"}
		      };
		$.messager.confirm("提示", "你确定要删除该会议室吗？", function() {
			$.ajax({
				type : "POST",
				url : "/boardroom/delete_boardroom",
				data : {
					"br_id" : idbox.val()
				},
				error : function() {
					redirect_to("/");
				},
				success : function(data) {
					if (data.resultFlag == "success") {
						$("#addModal").modal('hide');
						$.messager.popup('删除会议室成功！');
						list(1)
					} else {
						$.messager.popup(data.error_msg);
					}
				}
			});
		});
	} else {
		$.messager.popup("请先选择一个会议室！");
	}
}

function to_qrcode() {
	var idbox = $("input[name='idbox']:checked");
	if (idbox.length > 0) {
		var url = "/boardroom/to_room_qrcode?room_id="+idbox.val();
		var url1 = "/boardroom/room_qrcode?room_id="+idbox.val();
		$("#modalWrapper").load(url, {}, function(response, status) {
			if (status == "error") {
				redirect_to("/");
			} else {
				$("#imgcode").attr("src", url1);
				$("#addModal1").modal();
			}
		});
	} else {
		$.messager.popup('请先选择一个会议室！')
	}
}
