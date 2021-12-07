'use strict';
odoo.define(function(require){
    require('web.dom_ready');
    var ajax = require('web.ajax');

    var button = $('#cronometro_id');

    var _cronometro = function(){
        console.log('funciona');
    }
    button.click(_cronometro);
});