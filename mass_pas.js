$(window).on("load", function(){
	var map = new L.map("map_div", {
		zoomControl: true,
		center: [42.068317, -71.926237],
		zoom: 8
	});

	var vectorBasemap = L.tileLayer("http://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}", {
		attribution: "Tiles &copy; Esri &mdash; Source: Esri, DeLorme, HERE, MapmyIndia, &copy; OpenStreetMap contributors, and the GIS community"
	}).addTo(map);
});