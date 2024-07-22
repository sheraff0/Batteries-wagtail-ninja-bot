/*=============== HOME SWIPER ===============*/
let homeSwiper = new Swiper(".home-swiper", {
  spaceBetween: 30,
  loop: 'true',

  pagination: {
    el: ".swiper-pagination",
    clickable: true,
  },
})

class SwiperAutoScroll {
  constructor(swiper = homeSwiper, delay = 5000) {
    this.swiper = swiper;
    this.delay = delay;
    this.setEventListeners();
    this.setAutoScroll();
  }

  clearAutoScroll() { clearInterval(this.autoScroll) }

  setAutoScroll() {
    this.autoScroll = setInterval(() => this.swiper.slideNext(), this.delay)
  }

  setEventListeners() {
    this.swiper.on("touchStart", () => this.clearAutoScroll())
    this.swiper.on("touchEnd", () => this.setAutoScroll())
  }
}

const swiperAutoScroll = new SwiperAutoScroll(homeSwiper);
const nextButtons = document.querySelectorAll(".home-swiper .home__buttons .button__next");
nextButtons.forEach(button => button.addEventListener("click", () => homeSwiper.slideNext()));


/*=============== NEW SWIPER ===============*/
let newSwiper = new Swiper(".new-swiper", {
  centeredSlides: true,
  slidesPerView: "auto",
  loop: 'true',
  spaceBetween: 16,
});
