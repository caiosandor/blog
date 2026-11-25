document.addEventListener('DOMContentLoaded', () => {
    const el = document.getElementById('dados-mes');
    if (!el) return;

    const dados = JSON.parse(el.textContent);
    const ctx = document.getElementById('graf-mes');

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: dados.map(d => d.mes),
            datasets: [{
                label: 'Publicações criadas',
                data: dados.map(d => d.total),
                backgroundColor: '#2563eb',
                hoverBackgroundColor: '#1d4ed8',
                borderRadius: 6,
                maxBarThickness: 48
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: {
                    grid: { display: false }
                },
                y: {
                    beginAtZero: true,
                    ticks: { precision: 0 },
                    border: { dash: [4, 4] }
                }
            }
        }
    });
});