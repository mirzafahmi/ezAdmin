// Function to retrieve and update the breadcrumb stack
function updateBreadcrumbStack() {
    const currentUrl = window.location.href;
    let breadcrumbStack = JSON.parse(localStorage.getItem('breadcrumbStack')) || [];
    breadcrumbStack.push(currentUrl);
    localStorage.setItem('breadcrumbStack', JSON.stringify(breadcrumbStack));
}

// Function to get the breadcrumb stack
function getBreadcrumbStack() {
    return JSON.parse(localStorage.getItem('breadcrumbStack')) || [];
}
