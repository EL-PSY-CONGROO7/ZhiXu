document.getElementById('registerForm').addEventListener('submit', function (q) {
    q.preventDefault();

    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value.trim();
    const too_password = document.getElementById('confirm').value.trim();

    // 前端校验
    if (!username) {
        alert('请输入用户名！');
        return;
    }
    if (!/^[\u4e00-\u9fa5a-zA-Z0-9]+$/.test(username)) {
        alert('用户名只能包含中文、字母和数字!');
        return;
    }
    if (!password) {
        alert('请输入密码！');
        return;
    }
    if (password.length < 6) {
        alert('密码长度不能少于6位！');
        return;
    }
    if (password.length > 20) {
        alert('密码长度不能大于20位！');
        return;
    }
    if (!comfirm) {
        alert('请输入确认密码！');
        return;
    }
    if (password !== confirm) {
        alert('密码不一致！');
        return;
    }

    // 使用 axios 发送 application/x-www-form-urlencoded 格式
    const params = new URLSearchParams();
    params.append('username', username);
    params.append('password', password);
    params.append('confirm', too_password);

    axios({
        method: 'post',
        url: '/register',
        data: params,               // axios自动设置 Content-Type 为 application/x-www-form-urlencoded
        withCredentials: true        // 允许携带 cookie 保持 session
    })
    .then(function (response) {
        const data = response.data;  // axios 自动解析响应文本
        if (data === 'success') {
            alert('注册成功，即将跳转到登录页面');
            window.location.href = 'enter.html';
        } else if (data === 'failed') {
            alert('注册失败，请检查用户名是否已存在或者密码是否一致');
        }
    })
    .catch(function (error) {
        console.error('请求错误：', error);
        alert('网络错误，无法连接到服务器');
    });
});