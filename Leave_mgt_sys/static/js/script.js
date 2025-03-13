document.addEventListener("DOMContentLoaded", function () {
    const sidebarToggle = document.getElementById("sidebar-toggle");
    const sidebar = document.getElementById("sidebar");
    const navbar = document.querySelector(".stu-navbar");

    sidebarToggle.addEventListener("click", function () {
        sidebar.classList.toggle("collapsed");
        navbar.classList.toggle("collapsed");
    });
});
