const ctx = document.getElementById('productChart').getContext('2d');
const productData = JSON.parse('{{ product_data|tojson|safe }}');
new Chart(ctx, {
    type: 'bar',
    data: {
        labels: productData.map(item => item[0]),
        datasets: [{
            label: 'Number of Quotations',
            data: productData.map(item => item[1]),
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});
