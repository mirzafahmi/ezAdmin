function breadCrumbs() {
    document.addEventListener('DOMContentLoaded', function () {
        // Get a reference to the container where breadcrumbs will be rendered
        var breadcrumbsContainer = document.getElementById('breadcrumbs-container');
  
        // Function to get breadcrumbs based on the current URL
        function getBreadcrumbs() {
          var path = window.location.pathname;
      
          // Split the path into segments
          var segments = path.split('/').filter(Boolean);
  
          var breadcrumbs = [{ label: "Home", url: "/" }];
      
          // Capitalize the first letter of each segment
          for (var i = 0; i < segments.length; i++) {
            var segment = segments[i];
            var formattedSegment = segment.replace(/_/g, ' ')
                                          .replace(/\b\w/g, function(match) {
                                              return match.toUpperCase();
                                          });
            
            // Construct the URL up to the current level
            var url = '/' + segments.slice(0, i + 1).join('/');
    
            breadcrumbs.push({
                'label': formattedSegment,
                'url': url
            });
          }
          return breadcrumbs;
        }
  
        // Function to render breadcrumbs in the container
        function renderBreadcrumbs(breadcrumbs) {
            breadcrumbsContainer.innerHTML = ''; // Clear existing content
          if (breadcrumbs.length > 1) {
            // Iterate over the breadcrumbs to create <li> elements
            breadcrumbs.forEach(function (breadcrumb, index) {
                // Create a new <li> element
                var listItem = document.createElement('li');
                listItem.className = 'breadcrumb-item';
  
                // Create a new <a> element
                var link = document.createElement('a');
                link.href = breadcrumb.url;
                link.textContent = breadcrumb.label;
                if (breadcrumb.label == 'Home') {
                  link.id = "homePage";
                  const icon = document.createElement("i");
                  icon.className = "fa-solid fa-house me-2";
                  link.insertBefore(icon, link.firstChild);
                }
                
                // Append the <a> element to the <li> element
                listItem.appendChild(link);
  
                // Append the <li> element to the breadcrumbsContainer
                breadcrumbsContainer.appendChild(listItem);
  
                if (index === breadcrumbs.length - 1) {
                  listItem.classList.add('custom-active');
                  //listItem.setAttribute('aria-current', 'page');
              }
            });
          }
        }
  
        // Get and render breadcrumbs when the page loads
        var initialBreadcrumbs = getBreadcrumbs();
        renderBreadcrumbs(initialBreadcrumbs);
        
        var lastBreadcrumbLink = breadcrumbsContainer.querySelector('li:last-child a');
  
        // Add the custom class to the last breadcrumb link
        lastBreadcrumbLink.classList.add('custom-active');
        
      });
}