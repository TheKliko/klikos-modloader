function toggle_navigation() {
    var navigation = document.getElementById("header-navigation");
    if (navigation.classList.contains("active")) {
        navigation.classList.remove("active");
    } else {
        navigation.classList.add("active");
    }
}