const WEBSITE_VERSION = '1.1.2';
const MINIMUM_WIDTH = 1280;

window.onload = function onload() {
    const BODY = document.getElementsByTagName('body')[0];
    const DARKMODE = localStorage.getItem('darkmode');

    if (DARKMODE == 'true') {
        BODY.classList.add('darkmode');
    }

    const WEBSITE_VERSION_INDICATOR = document.getElementById('website-version-indicator');
    WEBSITE_VERSION_INDICATOR.innerHTML = WEBSITE_VERSION;

    if (window.innerWidth < MINIMUM_WIDTH) {
        alert(`Warning: This website was made for screens with a minimum width of ${MINIMUM_WIDTH}px. You have a detected screen width of ${window.innerWidth}px. Things may not look as expected.`)
    }
};

function fetch_latest_release() { // Generated by ChatGPT
    fetch('https://api.github.com/repos/thekliko/klikos-modloader/releases/latest')
        .then(response => response.json())
        .then(data => {
            const downloadUrl = data.assets[0].browser_download_url;
            window.location.href = downloadUrl;
        })
        .catch(error => {
            console.error('Error fetching latest release:', error);
            alert('Error fetching latest release')
        });
}

function toggle_darkmode() {
    const BODY = document.getElementsByTagName('body')[0];

    if (BODY.classList.contains('darkmode')) {
        BODY.classList.remove('darkmode');
        localStorage.setItem('darkmode', false);
    }
    else {
        BODY.classList.add('darkmode');
        localStorage.setItem('darkmode', true);
    }
}