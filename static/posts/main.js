//공개 및 학급 선택
public = document.querySelector('#id_public');
classroom = document.querySelector('#id_classroom');
postPublicTooltip = document.querySelector('#id_postPublicTooltip');
saveBtn = document.querySelector('#id_saveBtn');


function postPublicCheck() {
    if (public.value == 'public') {
        postPublicTooltip.setAttribute('data-tip', "누구나 일기를 읽을 수 있어요");
    } else if (public.value == 'class') {
        postPublicTooltip.setAttribute('data-tip', "선택한 학급에만 일기가 공개돼요");
    } else if (public.value == 'private') {
        classroom.value = '';
        postPublicTooltip.setAttribute('data-tip', "나만 일기를 읽을 수 있어요");
    }
}

public.addEventListener('change', postPublicCheck);
classroom.addEventListener('change', postPublicCheck);