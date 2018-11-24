console.log('Hola mundo');

(function() {
document.querySelector('.navbar-burger').addEventListener("click", toggleNav);

    function toggleNav() {
            nav = document.querySelector('.navbar-menu');
            if(nav.className === "navbar-menu") {
                nav.className = "navbar-menu is-active";
            } else {
                nav.className = "navbar-menu";
            }
    }
})();