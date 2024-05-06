// const body = document.querySelector('#body');
// const btn = document.querySelector('#darkmode-btn');
// const icon = document.querySelector('#darkmode-btn__icon');
// const toggle = document.querySelector('#darkmode-toggle');

//to save the dark mode use the object "local storage".

//function that stores the value true if the dark mode is activated or false if it's not.
function store(value){
    localStorage.setItem('darkmode', value);
}

//function that indicates if the "darkmode" property exists. It loads the page as we had left it.
// function load(){
//     const darkmode = localStorage.getItem('darkmode');

//     const body = document.querySelector('#body');
//     const btn = document.querySelector('#darkmode-btn');
//     const icon = document.querySelector('#darkmode-btn__icon');
//     const toggle = document.querySelector('#darkmode-toggle');

//     //if the dark mode was never activated
//     if(!darkmode){
//         store(false);
//         icon.classList.add('fa-sun');
//     } else if( darkmode == 'true'){ //if the dark mode is activated
//         body.classList.add('darkmode');
//         body.classList.add('darkmode-toggle');
//         icon.classList.add('fa-moon');
//     } else if(darkmode == 'false'){ //if the dark mode exists but is disabled
//         icon.classList.add('fa-sun');
//     }
// }

window.onload = function load() {
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

// btn.addEventListener('click', () => {

//     body.classList.toggle('darkmode-toggle');
//     icon.classList.add('animated');

//     //save true or false
//     store(body.classList.contains('darkmode-toggle'));

//     if(body.classList.contains('darkmode-toggle')){
//         icon.classList.remove('fa-sun');
//         icon.classList.add('fa-moon');
//     }else{
//         icon.classList.remove('fa-moon');
//         icon.classList.add('fa-sun');
//     }

//     setTimeout( () => {
//         icon.classList.remove('animated');
//     }, 500)
// })

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