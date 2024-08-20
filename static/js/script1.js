// Select the loader element
var loader_div = document.querySelector('.loader-div');

// Show the loader when the DOM is fully loaded
document.addEventListener("DOMContentLoaded", function() {
    loader_div.style.display = 'none';
});

// Function to check if all images are loaded
function imagesLoaded() {
    const images = document.querySelectorAll('img');
    let loadedCount = 0;

    images.forEach(image => {
        if (image.complete) {
            loadedCount++;
        } else {
            image.addEventListener('load', function() {
                loadedCount++;
                if (loadedCount === images.length) {
                    loader_div.style.display = 'none';

                }
            });
            image.addEventListener('error', function() {
                loadedCount++;
                if (loadedCount === images.length) {
                    loader_div.style.display = 'none';

                }
            });
        }
    });

    // In case all images are already loaded
    if (loadedCount === images.length) {
        loader_div.style.display = 'none';
    }
}

// Check if all images are loaded on window load
window.addEventListener("load", imagesLoaded);






var nav_btn = document.querySelector('#nav-btn');
var nav_btn_img = document.querySelector('#heroimgmob');
var navbar = document.querySelector('#navbar-mob');
var nav_btn_close = document.querySelector('#nav-btn-close');


const nav_items = document.querySelectorAll('.nav-link');

function removeActiveLink()
{
    
    nav_items.forEach((elem, index) => {
        elem.classList.remove('active-link');
        console.log(index);
    });

}


nav_items.forEach((elem, index) => {
    elem.addEventListener('click', () => {
        removeActiveLink(); 
        elem.classList.add('active-link');
        console.log(index);

        
        gsap.to('#navbar-mob',{
            x: '-100%',
        });
        
        navbar.style.display = 'none';
        navbar.style.left = '-70%';
        navbar.style.position = 'absolute';
        nav_btn.style.display = 'block';
        nav_btn_close.style.display = 'none';
        gsap.to('#nav-btn',{
            y:10,
            duration:0.2,
            opacity:1,
            
        });
    });
});


const sections = document.querySelectorAll('.section');
const navLinks = document.querySelectorAll('.nav-link');

const observer = new IntersectionObserver(
    (entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                navLinks.forEach(link => {
                    link.classList.toggle('active-link', link.getAttribute('href').substring(1) === entry.target.id);
                });
            }
        });
    },
    {
        root: null, // Use the viewport as the container
        rootMargin: '0px',
        threshold: 0.5 // Adjust based on when you want the link to become active
    }
);

sections.forEach(section => {
    observer.observe(section);
});


/*Click Navbar Btn */

nav_btn.addEventListener('click', () => {
    const timeline = gsap.timeline();

    timeline.to('#nav-btn', { y: -20, opacity: 0, duration: 0.2 })
        .to('#nav-btn-close', { rotation: 360, duration: 0.5, delay: 0.3 })
        .to('#navbar-mob', { x: '100%' }, "<")
        .from('#heroimg', { x: -200, opacity: 0, scale: 0.5, duration: 0.8 }, "<")
        .from('#heroname', { x: 200, opacity: 0, scale: 0.5, duration: 0.8 }, "<")
        .from('#loginbtn', { x: -200, opacity: 0, scale: 0.5, duration: 0.8 }, "<")
        .from('.nav-contact', { x: 100, opacity: 0, duration: 0.2, stagger: 0.1 }, "<")
        .from('#nav-links-list .nav-item', { x: -100, opacity: 0, scale: 0.5, stagger: 0.1 }, "<")
        .from('#contact-icons .icon', { x: 200, opacity: 0, stagger: 0.2 }, "<");

    navbar.style.display = 'flex';
    navbar.style.position = 'fixed';
    nav_btn.style.display = 'none';
    nav_btn_close.style.display = 'block';
});


nav_btn_close.addEventListener('click', () => {
    const timeline = gsap.timeline();

    timeline.to('#nav-btn-close', { opacity: 1, y: -10, rotation: -360, duration: 0.5 })
        .to('#navbar-mob', { x: '-100%' })
        .to('#nav-btn', { y: 10, opacity: 1, duration: 0.2 }, "<");

    navbar.style.display = 'none';
    navbar.style.position = 'absolute';
    nav_btn.style.display = 'block';
    nav_btn_close.style.display = 'none';
});







/* Animations */
const timeline = gsap.timeline({ delay: 0.5 });

timeline.from('#heroimg-desk', { x: -100, opacity: 0, scale: 0.5, duration: 0.5 })
    .from('#heroname-desk', { x: 100, opacity: 0, scale: 0.5, duration: 0.5 }, )
    .from('#loginbtn', { x: -200, opacity: 0, scale: 0.5, duration: 0.8 }, "<")
    .from('.nav-contact-desk', { x: 100, opacity: 0, duration: 0.2, stagger: 0.1 }, "<")
    .from('#nav-links-list-desk .nav-item', { x: -100, opacity: 0, scale: 0.5, stagger: 0.1 }, "<")
    .from('#contact-icons-desk .icon', { x: 200, opacity: 0, stagger: 0.2 }, "<");



