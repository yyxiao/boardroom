// 显示tree
function org_show(){
    var target=$("#orgTree");
    target.show();
}
//选择时回调函数
function zTreeOnCheck(event, treeId, treeNode) {
	if($("#search_org_id").val()==treeNode.id){
		$("#search_org_id").val('');
		$("#search_org_name").val('')
	}else {
		$("#search_org_id").val(treeNode.id);
		$("#search_org_name").val(treeNode.name);
	}
	$("#orgTree").hide();
};
//任何地方点击都隐藏orgTree
$(document).click(function(){
    $("#orgTree").hide();
});
//orgTree、org_id阻止事件
$("#orgTree").click(function(event){
    event.stopPropagation();
});
$("#search_org_name").click(function(event){
    event.stopPropagation();
});

function beforeCheck(treeId, treeNode) {
	return (treeNode.doCheck !== false);
}