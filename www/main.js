// Fetch data from the API
fetch('/api')
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        // Get the card template and the status bar tick template
        const cardTemplate = document.querySelector('.container template');
        const tickTemplate = cardTemplate.content.querySelector('.card--status--bar template');

        // For each service in the data
        data.forEach(service => {
            // if currentStatus is not present set it as undefined
            if (!service.currentStatus) {
                service.currentStatus = undefined;
            }

            // If statuses is not present set it as an empty array
            if (!service.statuses) {
                service.statuses = [];
            }

            // Clone the card template
            const card = document.importNode(cardTemplate.content, true);

            // Fill in the service name and current status
            card.querySelector('h3').textContent = service.name;
            card.querySelector('.card--status--dot circle').setAttribute('fill', getStatusColor(service.currentStatus));

            // For each status at 1 hour interval in the last 24 hours
            service.statuses.forEach(status => {
                // Clone the status bar tick template
                const tick = document.importNode(tickTemplate.content, true);

                // Set its class based on the status
                tick.querySelector('div').classList.add(`card--status--bar--tick--${getStatusClass(status)}`);

                // Append the cloned status bar tick to the status bar
                card.querySelector('.card--status--bar').appendChild(tick);
            });

            // Append the cloned card to the container
            document.querySelector('.container').appendChild(card);
        });
    })
    .catch(error => {
        console.log('Fetch failed:', error);
    });

// Function to get the status color
function getStatusColor(status) {
    switch (status) {
        case 'fail':
            return '#dc0000';
        case 'warning':
            return '#f1be00';
        case 'successful':
            return '#00a400';
        default:
            return 'dimgrey';
    }
}

// Function to get the status class
function getStatusClass(status) {
    switch (status) {
        case 'fail':
            return 'fail';
        case 'warning':
            return 'warning';
        case 'successful':
            return 'successful';
        default:
            return 'unchecked';
    }
}