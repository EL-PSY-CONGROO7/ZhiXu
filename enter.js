document.getElementById('loginForm').addEventListener('submit', async function(q) {
    q.preventDefault();

    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value.trim();

    // 强化空校验
    if (username === '') {
        alert('请输入用户名！');
        document.getElementById('username').focus();
        return;
    }
    if (!/^[\u4e00-\u9fa5a-zA-Z0-9]+$/.test(username)) {
        alert('用户名只能包含中文、字母和数字！');
        return;
    }
    if (password === '') {
        alert('请输入密码！');
        document.getElementById('password').focus();
        return;
    }

    try {
        // 使用 axios 发送 POST 请求
        const response = await axios({
            method: 'post',
            url: '/login',
            data: { username, password },   // 自动转为 JSON
            withCredentials: true            // 对应 fetch 的 credentials: 'include'
        });

        const data = response.data;          // axios 自动解析响应文本

        if (data === 'success') {
            alert('登录成功！');
            window.location.href = '/index2';
        } else {
            alert('登录失败，用户名或密码错误');
            document.getElementById('password').value = ''; // 清空密码框
        }
    } catch (error) {
        console.error('登录请求出错：', error);
        alert(`网络或服务器异常：${error.message}，请稍后再试`);
    }
});