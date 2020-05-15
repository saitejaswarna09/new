$(document).ready(function () {

  // NAVBAR TOGGLE OPEN AND CLOSE
  $('.menu').on('click', function () {
    $(this).toggleClass('open');
    $('.navbar').toggleClass('open');
  });

  $('.navbar .link').on('click', function () {
    $('.menu').removeClass('open');
    $('.navbar').removeClass('open');
  });

  // GSAP ANIMATIONS LANDING PAGE
  gsap.fromTo('.gradient-clipped', {scaleX: 0}, {duration: 1, scaleX: 1});
  gsap.fromTo('.logo', {x: -200, opacity: 0}, {duration: 1, delay: 0.5, x: 0, opacity: 1});
  gsap.fromTo('.menu', {opacity: 0}, {duration: 2, delay: 0.5, opacity: 1});
  gsap.fromTo('.gradient-textbox', {yPercent: 40, opacity: 0}, {duration: 1, delay: 0.8, yPercent: -50, opacity: 1});
});

//SMOOTHSCROLL FOR NAVBAR
$('.navbar a').on('click', function (e) {
  if (this.hash !== '') {
    e.preventDefault();

    const hash = this.hash;

    $('html, body')
      .animate({
        scrollTop: $(hash).offset().top
      },1500);
  }
});

const EducatorButton = document.getElementById('Educator');
const StudentButton = document.getElementById('Student');
const container = document.getElementById('container');

EducatorButton.addEventListener('click', () => {
  container.classList.add("right-panel-active");
});

StudentButton.addEventListener('click', () => {
  container.classList.remove("right-panel-active");
})

var mySwiper = new Swiper('.swiper-container', {
    // Optional parameters
    direction: 'vertical',
    loop: true,

    // If we need pagination
    pagination: {
        el: '.swiper-pagination',
    },

    // Navigation arrows
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },

    // And if we need scrollbar
    //scrollbar: {
    //    el: '.swiper-scrollbar',
    //},
})
