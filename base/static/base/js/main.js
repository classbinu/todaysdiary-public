//반응형 버거 메뉴
function toggleMenu() {
    burgerMenu = document.querySelector('#burgerMenu');
    
    burgerMenu.classList.toggle("hidden");
}
burgerButton = document.querySelector('#burgerButton');
burgerButton.addEventListener("click", toggleMenu);


//신고 후 얼럿
function reportAlert() {
    alert("의견이 제출되었습니다 :)");
}
report = document.querySelector('#reportBtn');
report2 = document.querySelector('#report2Btn');
report.addEventListener('click', reportAlert);
report2.addEventListener('click', reportAlert);