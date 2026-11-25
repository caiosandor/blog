document.addEventListener('DOMContentLoaded', () => {
    const el = document.getElementById('dados-mes');
    if (!el) return;

    // Desserializa o JSON injetado pelo template Django e renderiza o gráfico
    const dados = JSON.parse(el.textContent);
    new Chart(document.getElementById('graf-mes'), {
        type: 'bar',
        data: {
            labels: dados.map(d => d.mes),
            datasets: [{
                label: 'Posts por mês',
                data: dados.map(d => d.total),
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: { beginAtZero: true, ticks: { precision: 0 } }
            }
        }
    });
});