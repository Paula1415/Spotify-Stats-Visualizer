// $('body').append(
// 	'<div style="" id="loadingDiv"><div class="loader">Loading...</div></div>'
// );
// $(window).on('load', function () {
// 	$('#loadingDiv').show();
// 	setTimeout(removeLoader, 2000); //wait for page load PLUS two seconds.
// });
// function removeLoader() {
// 	$('#loadingDiv').fadeOut(500, function () {
// 		// fadeOut complete. Remove the loading div
// 		$('#loadingDiv').hide(); //makes page more lightweight
// 	});
// }

function showLoaderOnClick(url) {
	showLoader();
	window.location = url;
}

function showLoader() {
	$('body').append(
		'<div style="" id="loadingDiv"><div class="loader">Loading...</div></div>'
	);
	$(window).on('load', function () {
		$('#loadingDiv').show();
		setTimeout(removeLoader, 2000); //wait for page load PLUS two seconds.
	});
	function removeLoader() {
		$('#loadingDiv').fadeOut(500, function () {
			// fadeOut complete. Remove the loading div
			$('#loadingDiv').hide(); //makes page more lightweight
		});
	}
}
