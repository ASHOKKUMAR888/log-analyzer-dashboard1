document.getElementById('logUploadForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const formData = new FormData();
    formData.append('logFile', document.getElementById('logFile').files[0]);

    fetch('https://your-backend-url.com/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Handle the result
        console.log(data);
        const ctx = document.getElementById('errorChart').getContext('2d');
        const errorChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['Errors', 'Warnings', 'Info'],
                datasets: [{
                    data: [data.errors, data.warnings, data.info], // Replace with actual data
                    backgroundColor: ['red', 'yellow', 'green'],
                    borderWidth: 1
                }]
            }
        });
        document.getElementById('analysisResult').style.display = 'block';
    })
    .catch(error => console.error('Error:', error));
});
