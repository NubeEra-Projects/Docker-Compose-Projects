/**
 * Main JavaScript for the Microservice Demo Application
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all endpoint toggles
    initEndpointToggles();
    
    // Initialize "Try it out" functionality
    initTryItOut();
    
    // Initialize architecture diagram if it exists
    initArchitectureDiagram();
});

/**
 * Initialize collapsible endpoint documentation
 */
function initEndpointToggles() {
    const endpointHeaders = document.querySelectorAll('.endpoint-header');
    
    endpointHeaders.forEach(header => {
        header.addEventListener('click', function() {
            // Toggle the visibility of the endpoint content
            const content = this.nextElementSibling;
            if (content.style.display === 'block') {
                content.style.display = 'none';
            } else {
                content.style.display = 'block';
            }
        });
    });
}

/**
 * Initialize "Try it out" functionality for API endpoints
 */
function initTryItOut() {
    const tryItButtons = document.querySelectorAll('.try-it-btn');
    
    tryItButtons.forEach(button => {
        button.addEventListener('click', function() {
            const formSection = this.nextElementSibling;
            
            // Toggle form visibility
            if (formSection.style.display === 'block') {
                formSection.style.display = 'none';
                this.textContent = 'Try it out';
            } else {
                formSection.style.display = 'block';
                this.textContent = 'Cancel';
            }
        });
    });
    
    // Handle form submissions
    const apiForms = document.querySelectorAll('.api-form');
    
    apiForms.forEach(form => {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            
            const method = this.getAttribute('data-method');
            const endpoint = this.getAttribute('data-endpoint');
            const responseSection = this.nextElementSibling;
            const responseStatus = responseSection.querySelector('.response-status');
            const responseBody = responseSection.querySelector('.response-body');
            
            // Show loading state
            responseSection.style.display = 'block';
            responseStatus.innerHTML = '<div class="loading-spinner"></div> Loading...';
            responseBody.textContent = '';
            
            // Prepare request data
            let requestData = null;
            if (method !== 'GET' && method !== 'DELETE') {
                const jsonInput = this.querySelector('textarea[name="requestBody"]');
                if (jsonInput && jsonInput.value) {
                    try {
                        requestData = JSON.parse(jsonInput.value);
                    } catch (error) {
                        responseStatus.innerHTML = '<span class="text-error">Error: Invalid JSON</span>';
                        responseBody.textContent = error.message;
                        return;
                    }
                }
            }
            
            // Handle URL parameters
            let url = endpoint;
            const pathParams = this.querySelectorAll('input[name^="path_"]');
            pathParams.forEach(param => {
                const paramName = param.name.replace('path_', '');
                url = url.replace(`{${paramName}}`, param.value);
            });
            
            // Handle query parameters
            const queryParams = this.querySelectorAll('input[name^="query_"]');
            if (queryParams.length > 0) {
                const queryParts = [];
                queryParams.forEach(param => {
                    if (param.value) {
                        const paramName = param.name.replace('query_', '');
                        queryParts.push(`${paramName}=${encodeURIComponent(param.value)}`);
                    }
                });
                
                if (queryParts.length > 0) {
                    url += `?${queryParts.join('&')}`;
                }
            }
            
            // Make the API request
            makeApiRequest(method, url, requestData, responseStatus, responseBody);
        });
    });
}

/**
 * Make an API request to the specified endpoint
 */
function makeApiRequest(method, endpoint, requestData, statusElement, bodyElement) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    };
    
    if (requestData) {
        options.body = JSON.stringify(requestData);
    }
    
    fetch(endpoint, options)
        .then(response => {
            // Update status display
            const statusClass = response.ok ? 'text-success' : 'text-error';
            statusElement.innerHTML = `<span class="${statusClass}">${response.status} ${response.statusText}</span>`;
            
            return response.json();
        })
        .then(data => {
            // Display formatted response
            const formattedJson = JSON.stringify(data, null, 2);
            bodyElement.textContent = formattedJson;
            
            // Apply syntax highlighting if Prism.js is available
            if (typeof Prism !== 'undefined') {
                Prism.highlightElement(bodyElement);
            }
        })
        .catch(error => {
            statusElement.innerHTML = '<span class="text-error">Error</span>';
            bodyElement.textContent = error.message;
        });
}

/**
 * Initialize the architecture diagram SVG
 */
function initArchitectureDiagram() {
    const diagramContainer = document.getElementById('architecture-diagram');
    if (!diagramContainer) return;
    
    // The diagram is created using SVG directly in the HTML
    // This function could be used to add interactivity to the diagram
}
