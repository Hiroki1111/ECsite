from django import forms
from allauth.account.forms import SignupForm


class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='姓')
    last_name = forms.CharField(max_length=30, label='名')
    department = forms.CharField(max_length=30, label='所属', required=False)
    
# allauthのSignupFormを継承
class SignupUserForm(SignupForm):
    # サインアップ時に入力してほしい項目を記入
    first_name = forms.CharField(max_length=30, label="姓")  
    last_name  = forms.CharField(max_length=30, label="名")
    # なんでメールアドレスとパスワード入れないのか(すでに設定している？)
    
    # サインアップボタンがクリックされた時の動作を記入
    def save(self, request):
        user = super(SignupUserForm, self).save(request)  # ここ質問
        user.first_name = self.cleaned_data['first_name'] 
        user.last_name  = self.cleaned_data['last_name']
        user.save()
        return user