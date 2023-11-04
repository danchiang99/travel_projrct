
$(document).ready(function () {
    const content = $('.lightbox-content');
    const prevBtn = $('.prev-btn');
    const nextBtn = $('.next-btn');
    const refreshBtn = $('.refresh-btn');
    const itemHeight = 100;  // 假設每個項目的高度
    const itemsPerPage = 10;  // 每頁顯示的項目數量
    const dataItems = $('.lightbox-content .data-item');
    const maxPosition = (itemsPerPage - 2) * dataItems.outerHeight(true);
    let currentPosition = 0;

    // 函數：生成假的景點數據
    function generatePointItem(data, isFake) {
        const itemClass = isFake ? `data-item item-${data.id}` : 'data-item';
        const item = $(`<li class="${itemClass}"></li>`);
        item.append(`<img src="${data.imageUrl}" alt="景點圖片">`);
        item.append(`<div><p class="point-title">${data.title}</p><p class="point-text">${data.description}</p></div>`);
        return item;
    }

    // 在前端使用假資料
    function renderFakeData() {
        const content = $('.lightbox-content');
        for (const data of fakeData) {
            const item = generatePointItem(data);
            content.append(item);
        }
    }

    // 調用渲染函數
    renderFakeData();

    prevBtn.on('click', function () {
        currentPosition = Math.max(currentPosition - itemHeight * 2, 0);
        content.css('transform', `translateY(-${currentPosition}px)`);
    });

    nextBtn.on('click', function () {
        if (currentPosition + itemHeight * 2 < maxPosition) {
            currentPosition = Math.min(currentPosition + (itemHeight * 2), maxPosition - (itemHeight * 2));
            content.css('transform', `translateY(-${currentPosition}px)`);
        }
    });

    // 調整初始位置為第一個項目
    content.css('transform', `translateY(${currentPosition}px)`);



    // 函數：刷新燈箱內容
    function refreshLightbox() {
        content.empty();  // 清空原有內容
        currentPosition = 0;  // 重置位置
        // 動態生成假的景點項目並添加到燈箱
        for (let i = 1; i <= totalItems; i++) {
            const fakeData = generateFakeData(i);
            content.append(generatePointItem(fakeData));
        }
        content.css('transform', `translateY(${currentPosition}px)`); // 調整位置
    }

    // 初始加載，模擬獲取所有數據
    for (let i = 1; i <= 10; i++) {
        data.push(generateFakeData(i));
    }

    // 初始加載
    refreshLightbox();


    prevBtn.on('click', function () {
        currentPosition = Math.max(currentPosition - itemHeight * 2, 0);
        content.css('transform', `translateY(-${currentPosition}px)`);
    });

    nextBtn.on('click', function () {
        if (currentPosition + itemHeight * 2 < (totalItems - 1) * itemHeight) {
            currentPosition = Math.min(currentPosition + itemHeight * 2, (totalItems - 1) * itemHeight);
            content.css('transform', `translateY(-${currentPosition}px)`);
        }
    });

    // 刷新按鈕點擊事件
    refreshBtn.on('click', function () {
        refreshLightbox();
    });
});





$(document).ready(function () {
    const selectedItems = new Map();
    const maxSelectedItems = 5;
    const deleteAnimationDuration = 200; // 動畫持續時間，單位是毫秒

    function updateSelectedItemsArray() {
        const selectedItemsArray = Array.from(selectedItems.values());
        // 在這裡可以執行其他操作，比如將這個陣列傳送到後端
    }

    $('.data-item').click(function () {
        if (selectedItems.size < maxSelectedItems) {
            const itemId = $(this).data('id');

            if (!selectedItems.has(itemId)) {
                selectedItems.set(itemId, $(this).text());

                // 更新所選項目值的陣列
                updateSelectedItemsArray();

                const selectedItemElement = $('<li>').addClass('selected-item enter-from-left');
                selectedItemElement.attr('data-id', itemId);

                const imgElement = $(this).find('img').clone(); // 找到內部的 img 元素並複製它
                selectedItemElement.append(imgElement);

                const pointTitleElement = $(this).find('.point-title').clone(); // 找到內部的 .point-title 元素並複製它
                selectedItemElement.append(pointTitleElement);

                const cancelButton = $('<span class="cancel-button">×</span>');
                selectedItemElement.append(cancelButton);

                $('#selectPoints').append(selectedItemElement);
            }
        }
    });

    // 監聽取消按鈕的點擊事件
    // 在選中項目被刪除時，同時更新保存所選項目值的陣列
    $(document).on('click', '.cancel-button', function () {
        const canceledItemId = $(this).parent().data('id');
        const canceledItemElement = $(this).parent();

        // 顯示自訂對話框
        const dialog = document.getElementById('custom-dialog');
        dialog.style.display = 'flex';

        // 確定按鈕的點擊事件
        $(document).on('click', '#confirm-yes', function () {
            selectedItems.delete(canceledItemId); // 使用 Map 的 delete 方法來移除項目

            canceledItemElement.slideUp(deleteAnimationDuration, function () { // 使用指定的動畫秒數
                $(this).remove();

                setTimeout(function () {
                    updateSelectedItemsArray();
                }, 5000);

                // 調用更新所選項目值的陣列的函數
                updateSelectedItemsArray();

                const selectedItemsArray = Array.from(selectedItems.values());
            });


            // 隱藏對話框
            dialog.style.display = 'none';
            // 解除確定按鈕的點擊事件，避免多次綁定
            $(document).off('click', '#confirm-yes');
        });

        // 取消按鈕的點擊事件
        $(document).on('click', '#confirm-no', function () {
            dialog.style.display = 'none'; // 隱藏對話框

            // 解除取消按鈕的點擊事件，避免多次綁定
            $(document).off('click', '#confirm-no');
        });

    });



    // 送出按鈕點擊事件
    const fakeBackendEndpoint = '/fake-backend-endpoint';//指定後端端點
    $('#SubmitButton').click(async () => {
        const selectedItemsArray = Array.from(selectedItems.values());

        try {
            const response = await fetch('/fake-backend-endpoint', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                //指定HTTP請求或回應中包含的數據的類型。
                body: JSON.stringify({ selectedItems: selectedItemsArray })
            });

            if (response.ok) {
                // 處理成功回應
                console.log('資料成功送到後端');
            } else {
                // 處理錯誤回應
                console.error('資料送到後端時出現錯誤');
            }
        } catch (error) {
            console.error(error);
            // 處理錯誤
        }
    });
});
