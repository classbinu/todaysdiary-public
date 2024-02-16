from django import forms
from django.forms import TextInput, PasswordInput, EmailInput, Textarea
from .models import User

input = "input input-primary input-bordered my-2"

class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "nickname",
        ]
        widgets = {
            "username": TextInput(attrs={
                "class": input,
                "placeholder": "아이디 (4자리 이상의 소문자, 숫자)",
                "style": "width: 100%",
                "autofocus": "autofocus",
                "pattern": "^([a-z0-9_]){4,50}$",
            }),
            "nickname": TextInput(attrs={
                "class": input,
                "placeholder": "별명 (가입 후 바꿀 수 있어요)",
                "style": "width: 100%",
                "maxlengh": "20",
            }),
        }

    password = forms.CharField(widget=forms.PasswordInput(attrs={
            "class": input,
            "placeholder": "비밀번호 (8자리 이상)",
            "style": "width: 100%",
            "minlength": 8,
        })
    )
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
            "class": input,
            "placeholder": "비밀번호 확인",
            "style": "width: 100%",
            "minlength": 8,
        })
    )

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        if password != password1:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
        else:
            return password

    def clean_nickname(self):
        nickname = self.cleaned_data.get("nickname")
        if User.objects.filter(nickname=nickname).exists():
            raise forms.ValidationError("이미 존재하는 별명입니다.")
        else:
            return nickname

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        user.set_password(password)
        user.save()
        return super().save()


class MypageForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "nickname",
            "bio",
            "email",
        ]
        widgets = {
            "nickname": TextInput(attrs={
                "class": input,
                "placeholder": "별명",
            }),
            "bio": Textarea(attrs={
                "class": input,
                "placeholder": "자기소개",
            }),
        }

    email = forms.EmailField(widget=forms.EmailInput(attrs={
            "class": input,
            "placeholder": "이메일"
        })
    )

    def clean_nickname(self):
        nickname = self.cleaned_data.get("nickname")
        if User.objects.filter(nickname=nickname).exists():
            raise forms.ValidationError("이미 존재하는 별명입니다.")
        else:
            return nickname