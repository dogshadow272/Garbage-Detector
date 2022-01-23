const ctx = document.querySelector('#chart').getContext('2d');
console.log(data);
const myChart = new Chart(ctx, {
    type: 'line',
    data: {
        datasets: [{
            data
        }]
    }
});