function getChartsData() {
    let xhr = new XMLHttpRequest();
    xhr.onload = function() {
        if (this.readyState == 4 && this.status == 200) {
            let results = JSON.parse(xhr.responseText);
            console.log(results);
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


function constructCharts(data) {
    Object.keys(data).forEach(function(key) {
        
            // Split the text at "_"
            let keySplit = key.split("_");
            
            // Capitalize the first word
            let capitalizedFirstWord = keySplit[0][0].toUpperCase() + keySplit[0].slice(1);
            
            // Get the remaining of the text section
            let textSection = '';
            for (var i = 1; i < keySplit.length; i++) {
              textSection += keySplit[i] + ' ';
            }
            
            // Put together the capitalized text
            let capitalizedText = capitalizedFirstWord + ' ' + textSection;
            
            var ctx = document.getElementById(key).getContext('2d');
            var myChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
                    datasets: [{
                        label: capitalizedText,
                        data: [12, 19, 3, 5, 2, 3],
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
                                beginAtZero: true
                            }
                        }]
                    }
                }
            });
        }
    );
}
