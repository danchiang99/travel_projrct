// 取得今天的日期
const today = new Date().toISOString().split('T')[0];
// 將日期設定為出發日期的預設值
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById('date').value = today;
});

// 獲取當前時間
const now = new Date();
const hours = now.getHours().toString().padStart(2, '0');
const minutes = now.getMinutes().toString().padStart(2, '0');

// 設定時間選擇元件的預設值
const timeInput = document.getElementById('time');
timeInput.value = `${hours}:${minutes}`;

// 取得所有的 checkbox 元素
document.addEventListener("DOMContentLoaded", function () {
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    // 設定最大最小勾選數量
    const maxChecked = 4;
    const minChecked = 1;
    const submitButton = document.getElementById('SubmitButton'); //指定id 為 SubmitButton的送出按鈕

    // 監聽每個 checkbox 的變化
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            // 計算已勾選的 checkbox 數量
            const checkedCount = document.querySelectorAll('input[type="checkbox"]:checked').length;
            // 若已勾選數量超過最大值，取消勾選當前的 checkbox
            if (checkedCount > maxChecked) {
                checkbox.checked = false;
                alert(`最多只能選擇 ${maxChecked} 種類別`);
            }
        });
    });

    submitButton.addEventListener('click', (event) => {
        event.preventDefault();
        const checkedCount = Array.from(checkboxes).filter(checkbox => checkbox.checked).length;

        if (checkedCount < minChecked) {
            event.stopPropagation();
            alert(`請至少選擇 ${minChecked} 種類別`);
        } else {
            // 收集表單數據
            const formData = new FormData(document.getElementById('searchForm'));

            // 發送 POST 請求到 Flask 應用程序
            fetch('/submit', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (response.ok) {
                    // 可以在這裡處理成功提交後的操作
                    return response.text(); // 這裡假設後端返回一些文本作為成功消息
                } else {
                    alert('提交失敗'); // 如果提交失敗，可以顯示錯誤消息
                }
            })
            .then(data => {
                if (data) {
                    // 在前端顯示後端返回的成功消息
                    alert(data);
                    // 重定向到成功頁面，根據需要修改URL
                    window.location.href = '/submit';
                }
            })
            .catch(error => {
                console.error('錯誤：', error);
            });
        }
    });
});
