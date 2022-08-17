const renderChat2 = (data, labels) => {

    var ctx = document.getElementById('myChartt').getContext('2d');
    var myChart = new Chart(ctx, {
    type: 'line', 
    data: {
        labels: labels,
        datasets: [{
            label: 'Расходы за 6 месяцев',
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
    
});
};

const getChartData2 = () => {
    console.log("fetching");
    fetch('/expense_category_summary')
      .then((res) => res.json())
      .then((results) => {
        console.log("results", results);
        const category_date = results.expense_category_date;
        const [labels, data] = [
            Object.keys(category_date),
            Object.values(category_date),
        ];

        renderChat2(data, labels);

      });
};


document.onload = getChartData2();