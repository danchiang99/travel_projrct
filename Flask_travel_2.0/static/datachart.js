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

    const startHour = 0;
    const endHour = 23;
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

    // 設置初始時間為0點
    select.value = '00:00';
});


