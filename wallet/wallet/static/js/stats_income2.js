const renderChat3 = (data, labels) => {

    var ctx = document.getElementById('myChartt').getContext('2d');
    var myChart = new Chart(ctx, {
    type: 'polarArea', 
    data: {
        labels: labels,
        datasets: [{
            label: 'Доходы за последние 6 месяцев',
            data: data,
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
          }, 
        ],
    },
    options: {
        title: {
            display:true,
            text: 'Доходы за последние 6 месяцев',          
        },         
    },
    
});
};

const getChartData3 = () => {
    console.log("fetching");
    fetch('income_category_summary')
      .then((res) => res.json())
      .then((results) => {
        console.log("results", results);
        const category_date = results.income_category_date;
        const [labels, data] = [
            Object.keys(category_date),
            Object.values(category_date),
        ];

        renderChat3(data, labels);

      });
};


document.onload = getChartData3();