window.onload = ((e) => {
    let chartElement = document.getElementById("my-chart");

    let myChart = new Chart( chartElement, {
        type: "doughnut",
        options: {
            plugins: {
                title: {
                    display: true,
                    text: "Colors",
                }
            }
        },
        data: {
            labels: ["Aa", "Bb", "Cc", "Dd"],
            datasets: [{
                data: [1200, 1700, 800, 200],
                backgroundColor: ["rgba(255, 0, 0, 0.5)", "rgba(100, 255, 0, 0.5)", "rgba(200, 50, 255, 0.5)", "rgba(0, 100, 255, 0.5)"],
            }]
        },
    });

    myChart.render();
})
