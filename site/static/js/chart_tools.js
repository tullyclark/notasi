charts = []

function append_canvas(name, id){
	
	obj_str = "<div class='two-card'><h3>" + name +"</h3><canvas id='"+id+"'></canvas></div>"
	$('.row-cards').append(obj_str)
}

function init_chart(name, id, chart) {
	ctx = document.getElementById(id).getContext('2d');
	charts[id] = new Chart(
		ctx
		, { 
			type: chart.type
			, data: chart.data
		}
	)
}

function create_chart(name, id, chart) {
	if ($("#" + id)[0] == undefined) {
		append_canvas(name, id)
		init_chart(name, id, chart)
	}
}

function update_chart( id, chart) {
	if ($("#" + id)[0] != undefined) {
		charts[id].data.datasets = chart.data.datasets
		charts[id].update()
	}
}

function create_all_charts(charts) {
	$.each(charts, function( index, chart ) {
		create_chart(chart.name, chart.id, chart.chart);
	})
}

function update_all_charts(charts) {
	$.each(charts, function( index, chart ) {
		update_chart(chart.id, chart.chart);
	})
}