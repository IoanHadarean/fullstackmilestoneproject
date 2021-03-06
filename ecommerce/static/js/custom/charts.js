/* global Chart */

// Get HTML elements
var loaderDiv = document.getElementsByTagName('div')[3];
var header = document.getElementsByTagName('h1')[0];

// AJAX request for getting the charts data from the endpoint
function getChartsData() {
    loaderDiv.style.display = 'flex';
    let xhr = new XMLHttpRequest();
    xhr.onload = function() {
        if (this.readyState == 4 && this.status == 200) {
            let results = JSON.parse(xhr.responseText);
            loaderDiv.style.display = 'none';
            header.style.display = 'block';
            constructCharts(results);
        }
    };
    xhr.onerror = function() {
        console.log('Request error...');
    };
    xhr.open("GET", "/charts/data", true);
    xhr.send();
}

getChartsData();


// Construct the charts with the data received from the AJAX request
function constructCharts(data) {

    // Iterate through the data and get the keys and values
    Object.keys(data).forEach(function(key) {

        var dataLabels = [];
        var dataValues = [];
        for (var i = 0; i < data[key].length; i++) {
            var dataLabel = Object.keys(data[key][i]).toString();
            var dataValue = Object.values(data[key][i]).toString();
            dataLabels.push(dataLabel);
            dataValues.push(dataValue);
        }

        // Split the text at "_"
        let keySplit = key.split("_");

        // Capitalize the first word
        let capitalizedFirstWord = keySplit[0][0].toUpperCase() + keySplit[0].slice(1);

        // Get the remaining of the text section
        let textSection = '';
        for (var j = 1; j < keySplit.length; j++) {
            textSection += keySplit[j] + ' ';
        }

        // Put together the capitalized text
        let capitalizedText = capitalizedFirstWord + ' ' + textSection;
        
        // Separate the charts for the orders and the sales based on customization
        if (key == 'orders_last_3_days' || key == 'orders_last_3_months') {
            var ctx_orders = document.getElementById(key).getContext('2d');
            var chart_orders = new Chart(ctx_orders, {
                type: 'line',
                data: {
                    labels: dataLabels,
                    datasets: [{
                        label: capitalizedText,
                        data: dataValues,
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.2)',
                            'rgba(54, 162, 235, 0.2)',
                            'rgba(255, 206, 86, 0.2)',
                            'rgba(75, 192, 192, 0.2)',
                            'rgba(153, 102, 255, 0.2)',
                            'rgba(255, 159, 64, 0.2)'
                        ],
                        borderColor: [
                            'rgba(255, 99, 132, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(255, 206, 86, 1)',
                            'rgba(75, 192, 192, 1)',
                            'rgba(153, 102, 255, 1)',
                            'rgba(255, 159, 64, 1)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        yAxes: [{
                            ticks: {
                                min: 0,
                                beginAtZero: true,
                                callback: function(value, index, values) {
                                    if (Math.floor(value) === value) {
                                        return value;
                                    }
                                }
                            }
                        }],
                    },
                    // Customize charts.js tooltips
                    tooltips: {
                        callbacks: {
                            label: function(tooltipItem, data) {
                                var value = data.datasets[0].data[tooltipItem.index];
                                var label = data.labels[tooltipItem.index];

                                if (value === 0.1) {
                                    value = 0;
                                }

                                return label + ': ' + value;
                            }
                        }
                    }
                }
            });
        }
        else {
            var ctx_sales = document.getElementById(key).getContext('2d');
            var chart_sales = new Chart(ctx_sales, {
                type: 'line',
                data: {
                    labels: dataLabels,
                    datasets: [{
                        label: capitalizedText,
                        data: dataValues,
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.2)',
                            'rgba(54, 162, 235, 0.2)',
                            'rgba(255, 206, 86, 0.2)',
                            'rgba(75, 192, 192, 0.2)',
                            'rgba(153, 102, 255, 0.2)',
                            'rgba(255, 159, 64, 0.2)'
                        ],
                        borderColor: [
                            'rgba(255, 99, 132, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(255, 206, 86, 1)',
                            'rgba(75, 192, 192, 1)',
                            'rgba(153, 102, 255, 1)',
                            'rgba(255, 159, 64, 1)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        yAxes: [{
                            ticks: {
                                min: 0,
                                beginAtZero: true,
                                // Append £ to yAxes values
                                callback: function(value, index, values) {
                                    if (Math.floor(value) === value) {
                                        return value + ' £';
                                    }
                                }
                            }
                        }],
                    },
                    // Customize charts.js tooltips
                    tooltips: {
                        callbacks: {
                            label: function(tooltipItem, data) {
                                var value = data.datasets[0].data[tooltipItem.index] + ' £';
                                var label = data.labels[tooltipItem.index];

                                if (value === 0.1) {
                                    value = 0;
                                }

                                return label + ': ' + value;
                            }
                        }
                    }
                }
            });
        }
    });
}
