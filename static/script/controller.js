function show_carro(){
	document.getElementById('panel_carro').style.display ='block';
	document.getElementById('panel_moto').style.display ='none';
}
function show_moto(){
	document.getElementById('panel_carro').style.display ='none';
	document.getElementById('panel_moto').style.display ='block';
}
function show_bicicleta(){
	document.getElementById('panel_carro').style.display ='none';
	document.getElementById('panel_moto').style.display ='none';
}
window.onload = function() { 
	if(document.getElementById('rb_carro').checked){
		console.log("rb_carro");
		show_carro();
	}
	if(document.getElementById('rb_moto').checked){
		console.log("rb_moto");
		show_moto();
	}
	if(document.getElementById('rb_bicicleta').checked){
		console.log("rb_bicicleta");
		show_bicicleta();
	}
};