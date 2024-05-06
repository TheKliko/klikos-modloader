const website_version = "website version: 0.5.1"
const min_width = 1610

function store(value){
    localStorage.setItem('darkmode', value);
}

window.onload = function load() {
    const website_version_container = document.getElementById('website-version-container');
    website_version_container.innerHTML = website_version;

    if (window.innerWidth < min_width) {
        alert(`Warning: This webpage was made for windows with a minimum width of ${min_width}px. You have a window width of ${window.innerWidth}px. Things may not look as expected.`)
    }



    const darkmode = localStorage.getItem('darkmode');

    const body = document.querySelector('#body');
    const btn = document.querySelector('#darkmode-btn');
    const icon = document.querySelector('#darkmode-btn__icon');
    const toggle = document.querySelector('#darkmode-toggle');

    //if the dark mode was never activated
    if(!darkmode){
        store(false);
        icon.classList.add('fa-sun');
    } else if( darkmode == 'true'){ //if the dark mode is activated
        body.classList.add('darkmode');
        body.classList.add('darkmode-toggle');
        icon.classList.remove('fa-sun');
        icon.classList.add('fa-moon');
    } else if(darkmode == 'false'){ //if the dark mode exists but is disabled
        icon.classList.add('fa-sun');
    }
}

function darkmode_toggle() {
    const body = document.querySelector('#body');
    const btn = document.querySelector('#darkmode-btn');
    const icon = document.querySelector('#darkmode-btn__icon');
    const toggle = document.querySelector('#darkmode-toggle');



    body.classList.toggle('darkmode-toggle');
    body.classList.toggle('darkmode');
    icon.classList.add('animated');

    //save true or false
    store(body.classList.contains('darkmode-toggle'));

    if(body.classList.contains('darkmode-toggle')){
        icon.classList.remove('fa-sun');
        icon.classList.add('fa-moon');
    }else{
        icon.classList.remove('fa-moon');
        icon.classList.add('fa-sun');
    }

    setTimeout( () => {
        icon.classList.remove('animated');
    }, 500)
}