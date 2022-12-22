
function createPie(id,booknames,bcount){
    Chart.defaults.font.size = 14;
    Chart.defaults.plugins.legend.position = 'none';
    Chart.defaults.plugins.title.position='bottom';
    Chart.defaults.plugins.legend.align = 'start';
    var ctx = document.getElementById(id).getContext('2d');  
    const data = {
        labels: booknames,
        datasets: [
          {
            label: 'Most Popular Books',
            data: bcount,
            backgroundColor: [
            'rgb(2, 27, 51)',
            'rgb(4, 44, 82)',
            'rgb(7, 67, 124)',
            'rgb(9, 93, 172)',
            'rgb(12, 125, 231)',
            ],
            hoverOffset: 4
        }
      ]
    };
    
    const config = {
      type: 'pie',
      data: data,
      options: {
        responsive: false,
        plugins: {
          title: {
              display: true,
              text: 'Most Popular Books'
          }
      } 
      },
    };
    const popularityChart = new Chart(ctx, config);
};

function createBar(id,booksqty,booksavail){
    var ctx1 = document.getElementById(id).getContext('2d');

    const labels = ['1', '2', '3', '4', '5'];
    const data1 = {
      labels: labels,
      datasets: [
        {
          label: 'Quantity',
          data:booksqty,
          backgroundColor: [
          'rgb(0, 223, 255,0.7)',
          'rgb(204, 255, 204,0.7)',
          'rgb(255, 255, 153,0.7)',
          'rgb(255, 153, 187,0.7)',
          'rgb(204, 153, 255,0.7)',
          ],
        },
        {
          label: 'Availability',
          data: booksavail,
          backgroundColor: [
          'rgb(0, 153, 255,0.7)',
          'rgb(153, 255, 204,0.7)',
          'rgb(255, 255, 102,0.7)',
          'rgb(255, 102, 153,0.7)',
          'rgb(133, 51, 255,0.7)',
          ],
        }
      ]
    };
    const config1 = {
      type: 'bar',
      data: data1,
      options: {
        indexAxis: 'y',
        elements: {
          bar: {
            borderWidth: 1,
          }
        },
        responsive: false,
        plugins: {
          legend: {
            position: 'none',
          },
          title: {
            display: true,
            text: 'Quantity and Availabilty of books'
          }
        }
      },
    };
    const quantityChart = new Chart(ctx1, config1);
};

let width, height, gradient;
function getGradient(ctx, chartArea) {
  const chartWidth = chartArea.right - chartArea.left;
  const chartHeight = chartArea.bottom - chartArea.top;
  if (!gradient || width !== chartWidth || height !== chartHeight) {
    // Create the gradient because this is either the first render
    // or the size of the chart has changed
    width = chartWidth;
    height = chartHeight;
    gradient = ctx.createLinearGradient(0, chartArea.bottom, 0, chartArea.top);
    gradient.addColorStop(0, 'rgb(103, 0, 255)');
    gradient.addColorStop(0.5, 'rgb(64, 182, 221)');
    gradient.addColorStop(1,'rgb(180, 244, 249)' );
  }

  return gradient;
}

function createLine(weeklycount){
  var ctx = document.getElementById('issueChart').getContext('2d'); 
  Chart.defaults.plugins.legend.position = 'none';
  const labels = ['Day 1','Day 2','Day 3','Day 4','Day 5','Day 6','Day 7'];
  const data = {
    labels: labels,
    datasets: [{
      data: weeklycount,
      fill: false,
      borderColor: function(context) {
        const chart = context.chart;
        const {ctx, chartArea} = chart;

        if (!chartArea) {
          // This case happens on initial chart load
          return;
        }
        return getGradient(ctx, chartArea);
      },
      tension: 0.1
    }]
  };
  const config = {
    type: 'line',
    data: data,
    options:{
      scales: {
        y: {
          min: 0,
          ticks: {
            stepSize: 1
          }
        }
      }
    }
  };
  const issueChart = new Chart(ctx, config);
};

function createMemberLine(memberactivity){
  var ctx = document.getElementById('memberChart').getContext('2d');

  const data = {
    labels: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
    datasets: [
      {
        label: 'Member 1',
        data: memberactivity[0],
        borderColor: 'rgb(0, 153, 255)',
      },
      {
        label: 'Member 2',
        data: memberactivity[1],
        borderColor: 'rgb(153, 255, 204)',
        borderDash: [5, 5],
      },
      {
        label: 'Member 3',
        data: memberactivity[2],
        borderColor: 'rgb(255, 255, 102)',
        borderDash: [4, 4],
      },
      {
        label: 'Member 4',
        data: memberactivity[3],
        borderColor:  'rgb(255, 102, 153)',
        borderDash: [3, 3],
      },
      {
        label: 'Member 5',
        data: memberactivity[4],
        borderColor: 'rgb(133, 51, 255)',
        borderDash: [2, 2],
      }
    ]
  };
  const config = {
    type: 'line',
    data: data,
    options: {
      scales: {
        y: {
          ticks: {
            stepSize: 1
          }
        }
      },
      responsive: false,
      interaction: {
        mode: 'index',
        intersect: false
      },
      plugins: {
        legend: {
          position: 'none',
        },
        title: {
          display: true,
          text: 'Member Activity(Annual)'
        }
      }
    },
  };
  const memberChart = new Chart(ctx, config);
}