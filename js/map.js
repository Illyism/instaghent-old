var map;

function initialise() {
	var latlng = new google.maps.LatLng(51.0880844202022,3.72784376990969);
	var myOptions = {
		zoom: 13,
		center: latlng,
		mapTypeId: google.maps.MapTypeId.ROADMAP
	}
	map = new google.maps.Map(document.getElementById("map"), myOptions);
	collectImages()

}

function createMarker(standard_resolution, latlng) {
	var marker = new google.maps.Marker({position: latlng, map: map});
	google.maps.event.addListener(marker, "click", function() {
		if (infowindow) infowindow.close();
		infowindow = new google.maps.InfoWindow({content: ID});
		infowindow.open(map, marker);
	});
	return marker;
}

function collectImages() {
	var images = $(".shot");
	for (var i = images.length - 1; i >= 0; i--) {
		console.log(images[i])
		var location = $(images[i]).attr("data-location").split(",");
		createMarker($(images[i]).find("img").attr("src"), new google.maps.LatLng(location[0], location[1]))
	};
}

initialise()