// Bar chart
function draw_bar_chart2(element_id,
                         data,
                         options
) {
    // addBackgroundColorToDatasets(data['datasets'], color_kind);
    // dataset['backgroundColor'] =  utils.colors({count: dataset['label'].length, random: true});

    data['datasets'].forEach((dataset, dataset_index) =>
        dataset['backgroundColor'] = Array(dataset.data.length).fill(window.chartColors[options.colors[dataset_index]]));

    console.log(data);
    let chart = new Chart(document.getElementById(element_id), {
        type: 'bar',
        data: data,
        options: {
            legend: {display: false},
            title: {
                display: true,
                text: options.title
            },
            scales: {
                xAxes: [{
                    stacked: options.stacked,

                }],
                yAxes: [{
                    stacked: options.stacked,
                    scaleLabel: {
                        display: true,
                        labelString: options.yLabel
                    }
                }]
            }
        }
    });
    return chart
}

