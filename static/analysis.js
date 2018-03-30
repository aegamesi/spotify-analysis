$(document).ready(function() {
	$("#analysis").tablesorter({
		theme : "bootstrap",
		headerTemplate : '{content} {icon}',
		widgets : [ "uitheme" ],
	});
});