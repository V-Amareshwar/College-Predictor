
document.getElementById('prediction-form').addEventListener('submit', async function(e) {
    e.preventDefault();

    var form = e.target;
    var rank = form.rank.value;
    var category = form.category.value;
    var gender = form.gender.value;
    var branches = form.branches.value.split(',').map(function(b) { return b.trim(); }).filter(function(b) { return b; });
    var num_predictions = form.num_predictions.value;

    var loading = document.getElementById('loading');
    var error = document.getElementById('error');
    var table = document.getElementById('predictions-table');
    var tbody = document.getElementById('predictions-body');

    loading.style.display = 'block';
    error.style.display = 'none';
    table.style.display = 'none';
    tbody.innerHTML = '';

    try {
        var response = await fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                rank: parseInt(rank),
                category: category,
                gender: gender,
                preferred_branches: branches,
                num_predictions: parseInt(num_predictions)
            })
        });

        var data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to get predictions');
        }

        if (data.predictions && data.predictions.length > 0) {
            data.predictions.forEach(function(pred) {
                var row = document.createElement('tr');
                row.innerHTML = 
                    '<td>' + pred.college_name + '</td>' +
                    '<td>' + pred.branch + '</td>' +
                    '<td>' + Math.round(pred.predicted_closing_rank) + '</td>' +
                    '<td>' + pred.college_prestige.toFixed(2) + '</td>';
                tbody.appendChild(row);
            });
            table.style.display = 'table';
        } else {
            error.textContent = 'No predictions found for the given inputs.';
            error.style.display = 'block';
        }
    } catch (err) {
        error.textContent = 'Error: ' + err.message;
        error.style.display = 'block';
    } finally {
        loading.style.display = 'none';
    }
});
