'use strict';
odoo.define(function(require){
    require('web.dom_ready');
    var ajax = require('web.ajax');
    var button = $('#cronometro_id');
    var tiempo = document.getElementsByClassName("o_field_float o_field_number o_field_widget o_readonly_modifier");
    var tiempo_string = tiempo[0].innerText;
    tiempo_string = tiempo_string.split(':');
    var tiempo_actual = parseFloat(tiempo_string[0]);
    var tiempo_dos = parseFloat(tiempo_string[1]);
    console.log(tiempo_string)
    function temporizador(className, inicio, final, inicio2){
        this.class = className;
        this.inicio = inicio;
        this.final = final;
        this.contador = this.inicio;
        this.contador_seg = inicio2;

        this.conteoSegundos = function(){
            if(this.contador == -1){
                this.conteoSegundos = null;
                return;
            }
            this.classNames = document.getElementsByClassName(this.class);
            console.log('antes del if')
            console.log(this.contador)
            if(this.contador <= 9){
                if(this.contador_seg == 0){
                    if(this.contador != 0){
                        this.contador_seg = 60
                    }
                    this.classNames[0].innerText = '0' + this.contador-- + ':' + (this.contador_seg);
                }else{
                    if(this.contador_seg > 9){
                        this.classNames[0].innerText = '0' + this.contador + ':' + this.contador_seg--;
                    }else{
                        this.classNames[0].innerText = '0' + this.contador + ':0' + this.contador_seg--;
                    }
                }
            }else{
                if(this.contador_seg == 0){
                    if(this.contador != 0){
                        this.contador_seg = 60
                    }
                    this.classNames[0].innerText = this.contador-- + ':' + (this.contador_seg);
                }else{
                    if(this.contador_seg > 9){
                        this.classNames[0].innerText = this.contador + ':' + this.contador_seg--;
                    }else{
                        this.classNames[0].innerText = this.contador + ':0' + this.contador_seg--;
                    }
                }
            }
            setTimeout(this.conteoSegundos.bind(this),1000);
        };
    }
    var _functi = function(){
        let temporizador1 = new temporizador('o_field_float o_field_number o_field_widget o_readonly_modifier', tiempo_actual, 0, tiempo_dos) ;
        temporizador1.conteoSegundos()
    }
       button.click(_functi);
});