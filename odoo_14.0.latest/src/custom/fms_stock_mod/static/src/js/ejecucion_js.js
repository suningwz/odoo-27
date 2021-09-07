$('#time_end').click( function(){
       var output = document.getElementById('coordenadas');

			// Verificar si soporta geolocalizacion
			if (navigator.geolocation) {
				output.innerHTML = "<p>Tu navegador soporta Geolocalizacion</p>";
			}else{
				output.innerHTML = "<p>Tu navegador no soporta Geolocalizacion</p>";
			}

			//Obtenemos latitud y longitud
			function localizacion(position){
                alert('ingresa')
				var latitude = position.coords.latitude;
				var longitude = position.coords.longitude;

				var imgURL = "https://maps.googleapis.com/maps/api/staticmap?center="+latitude+","+longitude+"&size=600x300&markers=color:red%7C"+latitude+","+longitude+"&key=AIzaSyBRQN1Bqig3QMR2T32CFd1Eo03hLBQbi_I";

				output.innerHTML ="<img src='"+imgURL+"'>";



			}

			function error(){
				output.innerHTML = "<p>No se pudo obtener tu ubicación</p>";
			}

			navigator.geolocation.getCurrentPosition(localizacion,error);
    }
)