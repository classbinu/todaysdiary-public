//만14세 체크
location.href="#askAge";


//이용약관 동의
function policyAgree() {
    policyCheckbox = document.querySelector('#policyCheckbox');
    policyCheckbox.checked = true;
}
policyAgreeBtn = document.querySelector('#policyAgreeBtn');
policyAgreeBtn.addEventListener("click", policyAgree);


//개인정보 동의
function privacyAgree() {
    privacyCheckbox = document.querySelector('#privacyCheckbox');
    privacyCheckbox.checked = true;
}
privacyAgreeBtn = document.querySelector('#privacyAgreeBtn');
privacyAgreeBtn.addEventListener("click", privacyAgree);