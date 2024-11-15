document.addEventListener("DOMContentLoaded", function() {
    check_user_preference();
    set_darkmode();
});


function check_user_preference() {
    var body = document.getElementsByTagName("body")[0];
    if (window.matchMedia("(prefers-color-scheme: dark)").matches)  {
        body.classList.add("dark");
    } else {
        body.classList.remove("dark");
    };
};


function set_darkmode() {
    var theme = get_darkmode();
    var body = document.getElementsByTagName("body")[0];
    
    if (theme === "dark") {
        body.classList.add("dark");
    } else if (theme === "light") {
        body.classList.remove("dark");
    };
};


function toggle_darkmode() {
    var active = get_darkmode();
    return active == "true";
};


function get_darkmode() {
    var theme = localStorage.getItem("theme");
    return theme;
};


function toggle_darkmode() {
    var theme = get_darkmode();
    localStorage.setItem("theme", String(theme));
    set_darkmode();
};