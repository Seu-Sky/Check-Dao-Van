

document.addEventListener("DOMContentLoaded", function() {
    
    
    const form = document.getElementById("uploadForm");
    const loadingOverlay = document.getElementById("loadingOverlay");
    
    
    const btn = form ? form.querySelector("button[type='submit']") : null;

    if (form) {
        form.addEventListener("submit", function() {
           
            if (loadingOverlay) {
                loadingOverlay.style.display = "flex";
            }

            
            if (btn) {
                btn.innerHTML = "Đang xử lý..."; 
                btn.style.backgroundColor = "#95a5a6"; 
                btn.style.cursor = "not-allowed"; 
                btn.disabled = true; 
            }
        });
    }

});