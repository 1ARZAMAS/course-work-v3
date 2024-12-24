const menuToggle = document.querySelector('.menu-toggle');
const sidebar = document.querySelector('.sidebar');
const body = document.body;
const sidebarLinks = document.querySelectorAll('.sidebar-link');

menuToggle.addEventListener('click', (event) => {
    event.stopPropagation();
    sidebar.classList.toggle('active');
    body.classList.toggle('active');
    menuToggle.classList.toggle('hide');
    menuToggle.classList.remove('show');
});
sidebarLinks.forEach(link => {
    link.addEventListener('click', () => {
        sidebar.classList.remove('active');
        body.classList.remove('active');
        menuToggle.classList.remove('hide');
        menuToggle.classList.add('show');
    });
});

document.addEventListener('click', (event) => {
    if (!sidebar.contains(event.target) && !menuToggle.contains(event.target)) {
        sidebar.classList.remove('active');
        body.classList.remove('active');
        menuToggle.classList.remove('hide');
        menuToggle.classList.add('show');
    }
});