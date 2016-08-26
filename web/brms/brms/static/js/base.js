/*
 * 页面重定向
 */
function redirect_to(url){
	window.location = url
}

/*
 * 输入字符串是否含非法字符
 */
function is_str_unsafe(str){
	unsafe_str = " '~`·!@#$%^&*()-+./\"";
	for (i = 0; i < unsafe_str.length; i++){
		char = unsafe_str.charAt(i);
		position = str.indexOf(char);
		if (position != -1){
			return true
		}
	}
	return false
}
/*
 * 输入字符串是否超过长度
 */
function is_str_toolong(str, len){
	var len = arguments[1]?arguments[1]: 20;		//默认允许最大长度为20
	if (str.length > len){
		return true
	}else{
		return false
	}
}
/*
 * 初始化下拉复选框
 */
function init_multiselect(id) {
    $(id).multiselect({
    selectedClass: null,
      buttonText: function(options, select) {
        if (options.length == 0) {
          return '不计范围';
        }
        else {
            var selected = '';
            options.each(function() {
              var label = ($(this).attr('label') !== undefined) ? $(this).attr('label') : $(this).html();
 
              selected += label + ', ';
            });
            return selected.substr(0, selected.length - 2) ;
        }
      }
    });
  }


/**
 * 替换所有匹配exp的字符串为指定字符串
 * @param exp 被替换部分的正则
 * @param newStr 替换成的字符串
 */
String.prototype.replaceAll = function (exp, newStr) {
    return this.replace(new RegExp(exp, "gm"), newStr);
};

/**
 * 原型：字符串格式化
 * @param args 格式化参数值
 */
String.prototype.format = function(args) {
    var result = this;
    if (arguments.length < 1) {
        return result;
    }

    var data = arguments; // 如果模板参数是数组
    if (arguments.length == 1 && typeof (args) == "object") {
        // 如果模板参数是对象
        data = args;
    }
    for ( var key in data) {
        var value = data[key];
        if (undefined != value) {
            result = result.replaceAll("\\{" + key + "\\}", value);
        }
    }
    return result;
};