window.onload = ((e) => {
    let chartElement = document.getElementById("my-chart");
    let chartElement2 = document.getElementById("my-chart-2");

    let dataForChart = document.getElementById("data-for-chart");
            
    if (chartElement === null) return;

    if (dataForChart === null) return;

    let dataToDisplay = JSON.parse(dataForChart.dataset.chart.replaceAll("'", '"'));
    let colors = dataToDisplay[0].result.map(data => data.color_code);
    let colorPercentages = dataToDisplay[0].result.map(data => data.percent_count)
    
    let myChart = new Chart( chartElement, {
        type: "doughnut",
        options: {
            plugins: {
                title: {
                    display: true,
                    text: "Colors",
                }
            },
        },
        data: {
            labels: colors,
            datasets: [{
                data: colorPercentages,
                backgroundColor: colors,
            }],
            hoverOffset: 4,
        },
    });

    let myChart2 = new Chart( chartElement2, {
        type: "doughnut",
        options: {
            plugins: {
                title: {
                    display: true,
                    text: "Colors",
                }
            },
        },
        data: {
            labels: colors,
            datasets: [{
                data: colorPercentages,
                backgroundColor: colors,
            }],
            hoverOffset: 4,
        },
    });

    myChart.render();
    myChart2.render();

    window.updateChartDisplay = (dataSelected) => {
        colors = dataSelected.result.map(data => data.color_code);
        colorPercentages = dataSelected.result.map(data => data.percent_count);
        console.log(colors)
        console.log(colorPercentages)
        myChart2.data.labels = colors;
        myChart2.data.datasets[0].data = colorPercentages;
        myChart2.data.datasets[0].backgroundColor = colors;

        myChart2.update();
    }
})
