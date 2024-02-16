//공개 및 학급 선택
public = document.querySelector('#id_public');
classroom = document.querySelector('#id_classroom');
postPublicTooltip = document.querySelector('#id_postPublicTooltip');
postClassTooltip = document.querySelector('#id_postClassTooltip');



function postPublicCheck() {
    if (public.value == 'public') {
        classroom.removeAttribute('disabled');
        postPublicTooltip.setAttribute('data-tip', "누구나 일기를 읽을 수 있어요");
        postPublicTooltip.className = 'tooltip tooltip-open tooltip-top tooltip-info';

        postClassTooltip.setAttribute('data-tip', "학급을 선택하세요.");
        postClassTooltip.className = 'tooltip tooltip-open tooltip-top tooltip-info';

    } else if (public.value == 'class') {
        classroom.removeAttribute('disabled');
        postPublicTooltip.setAttribute('data-tip', "선택한 학급에만 일기가 공개돼요");
        postPublicTooltip.className = 'tooltip tooltip-open tooltip-top tooltip-success';

        postClassTooltip.setAttribute('data-tip', "학급을 선택하세요.");
        postClassTooltip.className = 'tooltip tooltip-open tooltip-top tooltip-success';

    } else if (public.value == 'private') {
        classroom.value = '';
        classroom.setAttribute('disabled', true);
        postPublicTooltip.setAttribute('data-tip', "나만 일기를 읽을 수 있어요");
        postPublicTooltip.className = 'tooltip tooltip-open tooltip-top tooltip-error';

        postClassTooltip.setAttribute('data-tip', "학급 선택 불가");
        postClassTooltip.className = 'tooltip tooltip-open tooltip-top tooltip-error';
    }
}

postPublicCheck();
public.addEventListener('change', postPublicCheck);
classroom.addEventListener('change', postPublicCheck);


// 임시 저장
tempPostLoad();
let autoSave = setInterval(tempPostSave, 1000);

function tempPostSave() {
    url = window.location.href;
    title = document.querySelector('#id_title').value;
    content = document.querySelector('textarea').value;
    localStorage.tempPostUrl = url;
    localStorage.tempPostTitle = title;
    localStorage.tempPostContent = content;
}

function tempPostLoad() {
    title = localStorage.tempPostTitle;
    content = localStorage.tempPostContent;
    if (title) {
        document.querySelector('#id_title').value = title;
    }
    if (content) {
        document.querySelector('textarea').value = content;
    }
}

function tempPostDelete() {
    clearInterval(autoSave);
    localStorage.removeItem('tempPostTitle');
    localStorage.removeItem('tempPostUrl');
    localStorage.removeItem('tempPostContent');
    this.setAttribute('disabled', true);
    document.forms["postForm"].submit();
}

saveBtn = document.querySelector('#id_saveBtn');
saveBtn.addEventListener('click', tempPostDelete);
