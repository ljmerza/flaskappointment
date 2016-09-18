'use strict'


var $newBtn =  $('#form-control-new');
var $cancelBtn = $('#form-control-cancel');
var $newForm = $('.newForm');



function getAppointments(searchString) {
	// erase results except for first child (theader)
	$('table#search-results > tbody > tr').not(':first').html('');

	// get data from server
	$.getJSON('/data', {
		'description': $('#search').val(), 
	}, function (data) {

		// for each results append to results table
		data.forEach( function (entry) {
			var day = moment.unix(entry.timedate).format("MMMM D")
			var time = moment.unix(entry.timedate).format("h:MMA")

			$('#search-results').append('<tr><td>'+day+'</td><td>'+time+'</td><td>'+entry.description+'</td></tr>');
		})
	})
}



$('#search-btn').click(function (event) {
	event.preventDefault();
	getAppointments($('#search').val());
})


$newBtn.click(newFormEvent);


$cancelBtn.click(function (event) {
	event.preventDefault();

	// reset form values
	$('#date').val('');
	$('#time').val('');
	$('#description').val('');

	// change new button back
	$newBtn.html('New');
	$newBtn.click(newFormEvent);

	// hide form
	$newForm.css('display', 'none');
})


function newFormEvent (event) {
	event.preventDefault();

	// change button text and show form
	$newBtn.html('Add');
	$newForm.css('display', 'block');

	// unbind click event
	$newBtn.off('click')


}