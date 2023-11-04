// 取得今天的日期
const today = new Date().toISOString().split('T')[0];
// 將日期設定為出發日期的預設值
document.addEventListener("DOMContentLoaded", function () {
    //以下三行為更新部份
    const dateInput = document.getElementById('date');
    dateInput.value = today;
    dateInput.min = today;
});

// 自動生成時間選項
document.addEventListener("DOMContentLoaded", function () {
    const select = document.getElementById('time');
    select.innerHTML = ''; // 清除現有的選項


    const startHour = 8;
    const endHour = 19;
    const interval = 30; // 30分鐘的間隔


    for (let hour = startHour; hour <= endHour; hour++) {
        for (let minute = 0; minute < 60; minute += interval) {
            const time = hour.toString().padStart(2, '0') + ':' + minute.toString().padStart(2, '0');
            const option = document.createElement('option');
            option.value = time; // 使用value屬性設定選項的值
            option.textContent = time;
            select.appendChild(option);
        }
    }
    // 添加20:00作為最後一個選項
    const lastOption = document.createElement('option');
    lastOption.value = '20:00';
    lastOption.textContent = '20:00';
    select.appendChild(lastOption);


    // 設置初始時間為8點
    select.value = '08:00';
});



//限制選取數量
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
                alert(`最多只能選擇 ${maxChecked}種類別`);
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
            const form = document.getElementById('searchForm');
            form.submit();
        }
    })

});
