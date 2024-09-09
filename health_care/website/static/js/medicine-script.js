document.addEventListener('DOMContentLoaded', function() {
    // Function to truncate text to a specified length
    function truncateText(text, length) {
        if (text.length > length) {
            return text.substring(0, length) + '...';
        }
        return text;
    }



    function searchMedicine() {
        const query = document.getElementById('searchInput').value;
        const url = new URL('/search/', window.location.origin);
        url.searchParams.append('query', query);

        fetch(url)
            .then(response => response.json())
            .then(data => {
                const flexContainer = document.getElementById('flexContainer');
                flexContainer.innerHTML = ''; // Clear current results

                if (data.results.length > 0) {
                    data.results.forEach(item => {
                        const div = document.createElement('div');
                        div.className = 'medicineflex-item';
                        div.innerHTML = `
                            <a href="/medicine/${item.id}/">
                            <h3>${item.product_name}</h3>
                            <p>${truncateText(item.medicine_desc, 100)}</p>
                            </a>
                        `;
                        flexContainer.appendChild(div);
                    });
                } else {
                    flexContainer.innerHTML = '<p>No medicines found.</p>';
                }
            })
            .catch(error => console.error('Error:', error));
    }


    // Attach search function to the input event
    document.getElementById('searchInput').addEventListener('keyup', searchMedicine);
});
