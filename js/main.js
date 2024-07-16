const website_version = '2.0.2';

// window.onload = function onload() {
document.addEventListener("DOMContentLoaded", function() {
    var version_container = document.getElementById('website-version')
    version_container.innerHTML = website_version

    set_darkmode();
});

function set_darkmode() {
    var darkmode = localStorage.getItem('darkmode');
    var body = document.getElementsByTagName('body')[0];

    if (darkmode === 'true') {
        body.classList.add('darkmode');
    } else {
        body.classList.remove('darkmode');
    };
};

function toggle_darkmode() {
    var darkmode = localStorage.getItem('darkmode');

    if (darkmode === 'true') {
        localStorage.setItem('darkmode', 'false');
    } else {
        localStorage.setItem('darkmode', 'true');
    };

    set_darkmode();
};

function hamburger_menu_toggle() {
    if (mobile_device()) {
        var navigation = document.getElementById('header-navigation');
        var hamburger = document.getElementById('header-hamburger');
        navigation.classList.toggle('active')
        hamburger.classList.toggle('active')
    };
};

function download_now() {
    if (mobile_device()) {
        alert('Download not available for mobile devices');
        return;
    };
    window.open('download.html');
};

function mobile_device() {
    return window.innerWidth <= 768;
};
