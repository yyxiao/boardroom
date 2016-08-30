/**
 * Created by cuizc on 16-8-8.
 */
var loadcontent = function(url) {
	$('#mainContent').load(url,function(response,status,xhr){
		if (status == 'error'){
				redirect_to("/login");
		}
	});
};
