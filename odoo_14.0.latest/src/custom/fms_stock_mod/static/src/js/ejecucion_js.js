'use strict'
odoo.define(function(require){
    require('web.dom_ready');
    var ajax = require('web.ajax');
    var button = $('#time_end');
    var name = document.getElementsByClassName('o_field_char o_field_widget o_readonly_modifier o_required_modifier');
    console.log(name[0].textContent);
    var _onbutton = function(e){
        if (navigator.geolocation) {
            function localizacion(position){
				var latitude = position.coords.latitude;
				var longitude = position.coords.longitude;
				ajax.jsonRpc('/ajax-geolocalizacion', 'POST', {
                    "latitude":latitude,
                    "longitud":longitude,
                    "name":name[0].textContent
                }).then(function(data){
                    console.log(data);
                    console.log('ingreso');
                });
			}
			function error(){
				console.log('error navigator');
			}
			navigator.geolocation.getCurrentPosition(localizacion,error);
		}else{
			console.log('Error geo');
		}
    }
    button.click(_onbutton);
});
