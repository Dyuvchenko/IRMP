document.addEventListener('DOMContentLoaded', () => {

    add_route_btn.onclick = () => {
        console.log("add_route_btn-click");
        window.location.href = '/map_add_route';
        return true;
    };

});