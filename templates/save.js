	$('submit').click(function(){
		var latlng = marker.getPosition();
		var lat = latlng.lat();
		var lng = latlng.lng()
		document.getElementById("lat1").value = lat
		document.getElementById("lng1").value = lng
	});


}

$(function(){
	$('button').click(function(){
		var user = $('#inputUsername').val();
		var pass = $('#inputPassword').val();
		$.ajax({
			url: '/signUpUser',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});