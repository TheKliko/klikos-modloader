const VERSION = "3.0.0";


document.addEventListener("DOMContentLoaded", function() {
    try {
        var span = document.getElementById("website-version-container")
        span.innerHTML = VERSION
    } catch (error) {
        console.log(`Failed to set version info! ${error}`);
    }
});