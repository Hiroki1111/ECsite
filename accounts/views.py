from django.shortcuts import render,redirect
from django.views import View
from .models import CustomUser
from .forms import ProfileForm, SignupUserForm
from allauth.account import views
from django.contrib.auth.mixins import LoginRequiredMixin


# LoginRequireMixinを追加することでプロフィール画面はログイン状態でないと遷移できないようになる
class ProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # ユーザー情報を取得
        user_data = CustomUser.objects.get(id=request.user.id)
        return render(request, 'accounts/profile.html', {
            'user_data':user_data,
        })
        

# LoginRequireMixinを追加することでプロフィール画面はログイン状態でないと遷移できないようになる
class ProfileEditView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_data = CustomUser.objects.get(id=request.user.id)
        form = ProfileForm(
            request.POST or None,
            # 編集フォームは初期データを入力しておく必要がある
            initial = {
                'first_name': user_data.first_name,
                'last_name': user_data.last_name,
                'address': user_data.address,
                'tell': user_data.tell,
            }
        )
        
        return render(request, 'accounts/profile_edit.html', {
            'form':form,
        })
        
    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST or None)
        if form.is_valid():
            # 最初にuser_dataを取得
            user_data = CustomUser.objects.get(id=request.user.id)
            # user_dataを使ってそれぞれの情報を取得
            user_data.first_name = form.cleaned_data['first_name']
            user_data.last_name = form.cleaned_data['last_name']
            user_data.address = form.cleaned_data['address']
            user_data.tell = form.cleaned_data['tell']
            # 入力データをデータベースに保存
            user_data.save()
            # 編集が完了したらprofile画面に遷移する
            return redirect('accounts:profile')
        
        return render(request, 'accounts/profile.html', {
            'form': form,
        })
        
# LoginViewを継承
class LoginView(views.LoginView):
    template_name = 'accounts/login.html'
    
    
# LogoutViewを継承
class LogoutView(views.LogoutView):
    template_name = 'accounts/logout.html'
    
    def post(self, *args, **kwargs):
         # userの認証状況
        if self.request.user.is_authenticated: 
            # ログイン状態だった場合ログアウト
            self.logout()
        # ログアウトしたらトップページへ遷移
        return redirect('/') 
    
    
# allauthのSignupViewを継承
class SignupView(views.SignupView):
    template_name = 'accounts/signup.html'
    # オリジナルのフォームを使用
    form_class = SignupUserForm # ここなに