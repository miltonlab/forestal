var configuracion_datatable = {
    oLanguage: {
	"sLengthMenu": "Mostrando _MENU_ elementos por página",
	"sInfo": "Mostrando del _START_ al _END_ de _TOTAL_ elementos",
	"sInfoEmpty": "Mostrando de 0 a 0 elementos",
	"sZeroRecords": "No se encontraron registros",
	"sInfoFiltered": "(filtrados de _MAX_ elementos en total)",
	"sSearch" : "Buscar:",
	//"bJQueryUI": false,
	//"bSortClasses": false,
	//"bScrollCollapse":true,
	oPaginate: {
	    "sFirst": "Primero",
	    "sLast": "Ultimo",
	    "sNext": "Siguiente",
	    "sPrevious": "Anterior"
	}
    },
    bPaginate: true,
    bLengthChange: true,
    bFilter: true,
    bSort: true,
    bInfo: true,
    bAutoWidth: true,
    sPaginationType: "full_numbers"

};

/* Menú principal */
function menu_ajax(url){
    jQuery.get(url,function(response){
	jQuery("#content").fadeOut(0);
	jQuery("#content").html(response).fadeIn(500);
    });
}

//Validacion de cajas de texto enteras con JS
function validar_entero(field){
    if ( field.value == "" ){
	return;
    }
    var value = parseInt(field.value);
    if ( isNaN(value) ){
	// Para accedder al espacio de mensajes
	var idmsg = parseInt(field.id);
	//var idmsg = field.id.split('-')[0] + "-msg";
	idmsg += "-msg";
	jQuery("#" + idmsg).html("ERROR.....").fadeIn('slow').addClass('error').fadeOut('slow');
	field.focus();
	value = "";
    }
    field.value = value;
}

//Validacion de cajas de texto decimales con JS
function validar_decimal(field){
    if ( field.value == "" ){
	return true;
    }
    var value = parseFloat(field.value);
    if ( isNaN(value) ){
	// Para accedder al espacio de mensajes
	// Busqueda del id independiente de acuerdo a los digitos
	// que contiene el id original
	var idmsg = "";
	for (var i=0; i<field.id.length;i++){
	    if (parseInt(field.id.charAt(i))){
		idmsg += field.id.charAt(i);
	    }
	}
	idmsg += "-msg";
	jQuery("#" + idmsg).html("ERROR.....").fadeIn('slow').addClass('error').fadeOut('slow');
	field.focus();
	value = "";
    }
    field.value = value;
}

function validar_texto(field){
    if ( field.value == "" ){
	return;
    }
    var val = parseFloat(field.value);
    // si es un numero el formato es incorrecto
    if ( ! isNaN(val) ){
	// Para accedder al espacio de mensajes
	// Busqueda del id independiente de acuerdo a los digitos
	// que contiene el id original
	var idmsg = "";
	for (var i=0; i<field.id.length;i++){
	    if (parseInt(field.id.charAt(i))){
		idmsg += field.id.charAt(i);
	    }
	}
	idmsg += "-msg";
	jQuery("#" + idmsg).html("ERROR.....").fadeIn('slow').addClass('error').fadeOut('slow');
	field.focus();
	value = "";
    }
    field.value = value;
}


// Cuando se carga /editmadera
function config_edit_madera(){
    jQuery(document).ready(function(){
	// Se aplica a todo lo que tenga un 'title'
	jQuery("*[title]").tipsy();

	jQuery('input.rango-entero').each(function (){
	    var t = jQuery(this);
	    t.attr('onblur','validar_entero(this);');
	});
	jQuery('input.rango-decimal').each(function (){
	    var t = jQuery(this);
	    t.attr('onblur','validar_decimal(this);');
	});
	jQuery('input.rango-texto').each(function (){
	    var t = jQuery(this);
	    t.attr('onblur','validar_texto(this);');
	});
	
	jQuery("#btnguardar").click(function(){
	    var resp = confirm('Está seguro que desea grabar los datos');
	    if (! resp) {
		window.location.href("#");
	    }else{
		jQuery.ajax({
		    type: "POST",
		    url: "/editmadera",
		    data: $('#form-madera').serializeArray(),
		    error: function(xhr,status){
			alert("Error al grabar madera: " + status + xhr);
		    }
		});
		jQuery('#content').html('<h3>  Madera grabada con Exito </h3>').slideDown(1000);
	    }
	});
	
	jQuery("input[name=selector-madera]").click(function(){
	    switch(this.value){
	    case 'codificar':
		// Se envía a codificar las propiedades en el servidor
		var resp = confirm('Toda la columna CODIFICACIONES se reemplazará en base a la columna VALORES');
		if (! resp){
		    return;
		}
		jQuery.ajax({
		    type: "GET",
		    url: "/codificar",
		    // se envia formulario decodificado
		    data: jQuery('#form-madera').serializeArray(),
		    dataType: 'json',
		    success: function(response){
			// response es un diccionario ..
			for (p in response){
			    var nombre_prop='prop-'+p;
			    jQuery("#" + nombre_prop).val(response[p]);
			};
			/// jQuery('#btnguardar').attr('disabled','false');
			jQuery('#btnguardar').each(function(){this.removeAttribute("disabled");});
		    },
		    error: function(xhr,status){
			alert('Ocurrió un error al enviar madera: ' + status);
		    }
		});
		//No hay break para propagar el siguiente case con una excepcion
		
	    case 'por_valor':
		// No se puede guardar aún
		// jQuery('#btnguardar').attr('disabled','true');
		jQuery("input[name^='valor']").each(function(){
		    this.removeAttribute("readonly");
		});
		jQuery("input[name^='prop']").each(function(){
		    this.setAttribute("readonly","readonly");
		    this.value = '';
		    //$(this).attr("readonly","readonly");
		    if (jQuery("input[name=selector-madera]").value == 'por_valor'){
			this.value = '';
		    };
		    
		});
		break;
		
	    case 'por_propiedad':
		// Listo para guardar
		//jQuery('#btnguardar').attr('disabled','false');
		jQuery('#btnguardar').each(function(){this.removeAttribute("disabled");});
		jQuery("input[name^='valor']").each(function(){
		    this.setAttribute("readonly","readonly");
		    this.value = '';
		});
		jQuery("input[name^='prop']").each(function(){this.removeAttribute("readonly");});
	    }
	});
	
    });
}
