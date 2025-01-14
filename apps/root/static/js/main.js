/*=============== SHOW MENU ===============*/
const navMenu = document.getElementById('nav-menu'),
  navToggle = document.getElementById('nav-toggle'),
  navClose = document.getElementById('nav-close')

/*===== MENU SHOW =====*/
/* Validate if constant exists */
if (navToggle) {
  navToggle.addEventListener('click', () => {
    navMenu.classList.add('show-menu')
  })
}

/*===== MENU HIDDEN =====*/
/* Validate if constant exists */
if (navClose) {
  navClose.addEventListener('click', () => {
    navMenu.classList.remove('show-menu')
  })
}

/*=============== REMOVE MENU MOBILE ===============*/
const navLink = document.querySelectorAll('.nav__link')

function linkAction() {
  const navMenu = document.getElementById('nav-menu')
  // When we click on each nav__link, we remove the show-menu class
  navMenu.classList.remove('show-menu')
}
navLink.forEach(n => n.addEventListener('click', linkAction))

/*=============== CHANGE BACKGROUND HEADER ===============*/
function scrollHeader() {
  const header = document.getElementById('header')
  // When the scroll is greater than 50 viewport height, add the scroll-header class to the header tag
  if (this.scrollY >= 50) header.classList.add('scroll-header'); else header.classList.remove('scroll-header')
}
window.addEventListener('scroll', scrollHeader)

/*=============== SCROLL SECTIONS ACTIVE LINK ===============*/
const sections = document.querySelectorAll('section[id]')

function scrollActive() {
  const scrollY = window.pageYOffset

  sections.forEach(current => {
    const sectionHeight = current.offsetHeight,
      sectionTop = current.offsetTop - 58,
      sectionId = current.getAttribute('id')
    const tabs = document.querySelector('.nav__menu a[href*=' + sectionId + ']');
    tabs && tabs.classList[
      scrollY > sectionTop && scrollY <= sectionTop + sectionHeight
        ? "add" : "remove"
    ]('active-link')
  })
}
window.addEventListener('scroll', scrollActive)

/*=============== SHOW SCROLL UP ===============*/
function scrollUp() {
  const scrollUp = document.getElementById('scroll-up');
  // When the scroll is higher than 460 viewport height, add the show-scroll class to the a tag with the scroll-top class
  if (this.scrollY >= 460) scrollUp.classList.add('show-scroll'); else scrollUp.classList.remove('show-scroll')
}
window.addEventListener('scroll', scrollUp)

/*=============== SCROLL REVEAL ANIMATION ===============*/
const sr = ScrollReveal({
  origin: 'top',
  distance: '60px',
  duration: 2500,
  delay: 400,
  // reset: true
})

sr.reveal(`.home-swiper, .new-swiper, .newsletter__container`)
sr.reveal(`.category__data, .catalog__content, .footer__content`, { interval: 100 })
sr.reveal(`.about__data, .discount__img`, { origin: 'left' })
sr.reveal(`.about__img, .discount__data`, { origin: 'right' })

/*=============== CONTACTS DIALOG ===============*/

class Dialog {
  constructor(buttonsSelector, dialogSelector) {
    this.buttonsSelector = buttonsSelector;
    this.dialogSelector = dialogSelector;
    this.buttons = document.querySelectorAll(buttonsSelector);
    this.dialog = document.querySelector(dialogSelector);
    this.close = document.querySelector(`${dialogSelector} button.button__close`);
    this.setListeners();
  }

  setListeners() {
    this.buttons.forEach(button => button.addEventListener("click", () => {
      this.dialog.showModal();
    }));
    this.close.addEventListener("click", () => {
      this.dialog.close();
    });
    document.body.addEventListener("click", e => {
      if (!e.target.closest(`div${this.dialogSelector}, ${this.buttonsSelector}`)) this.dialog.close();
    })
  }
}

const connectDialog = new Dialog(".button__connect", ".dialog__connect")
