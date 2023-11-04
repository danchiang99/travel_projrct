
//光箱效果
$(document).ready(function () {
    const content = $('.lightbox-content');
    const prevBtn = $('.prev-btn');
    const nextBtn = $('.next-btn');
    // const refreshBtn = $('.refresh-btn');
    const itemHeight = $('.data-item').outerHeight(true);
    const dataItems = $('.lightbox-content .data-item');
    // const totalItems = 50;
    const totalItems = $('.data-item').length;
    const maxPosition = (totalItems - 2) * dataItems.outerHeight(true);
    let currentPosition = 0;
    // let currentPage = 1; // 當前頁數
    // const totalPages = Math.ceil(allItems / totalItems); //總頁數

    prevBtn.on('click', function () {
        currentPosition = Math.max(currentPosition - itemHeight * 3, 0);
        content.css('transform', `translateY(-${currentPosition}px)`);
    });

    nextBtn.on('click', function () {
        if (currentPosition + itemHeight * 2 < maxPosition) {
            currentPosition = Math.min(currentPosition + (itemHeight * 3), maxPosition - (itemHeight * 2));
            content.css('transform', `translateY(-${currentPosition}px)`);
        }
    });

    // 調整初始位置為第一個項目
    content.css('transform', `translateY(${currentPosition}px)`);



    $(document).ready(function () {


        // 監聽滑鼠滾輪事件
        content.on('wheel', function (event) {
            event.preventDefault();

            // 獲取滾輪的 deltaY 值，正值表示向下滾動，負值表示向上滾動
            const deltaY = event.originalEvent.deltaY;

            // 計算新的位置
            currentPosition += deltaY;

            // 限制位置在合法範圍內
            currentPosition = Math.max(0, Math.min(currentPosition, (totalItems - 4) * dataItems.outerHeight(true)));

            // 調整光箱的位置
            content.css('transform', `translateY(-${currentPosition}px)`);
        });
    });




    $(document).ready(function () {
        const content = $('.lightbox-content');
        const dataItems = $('.lightbox-content .data-item');
        const itemHeight = dataItems.outerHeight(true);
        const totalItems = dataItems.length;
        const maxPosition = (totalItems - 4) * dataItems.outerHeight(true);
        let startPosition = 0;
        let touchStartY = 0;

        content.on('touchstart', function (event) {
            touchStartY = event.originalEvent.touches[0].clientY;
        });

        content.on('touchmove', function (event) {
            event.preventDefault();
            const touchMoveY = event.originalEvent.touches[0].clientY;
            const deltaY = touchMoveY - touchStartY;

            // 計算新的位置
            startPosition += deltaY;

            // 限制位置在合法範圍內
            startPosition = Math.max(0, Math.min(startPosition, maxPosition));

            // 調整光箱的位置
            content.css('transform', `translateY(-${startPosition}px)`);

            // 更新起始觸摸位置
            touchStartY = touchMoveY;
        });
    });

    
    // const pointTitleElements = document.querySelectorAll('.point-title');
    // let maxTextLength;

    // function updateMaxTextLength() {
    //     if (window.matchMedia("(max-width: 450px)").matches) {
    //         maxTextLength = 14;
    //     } else {
    //         maxTextLength = 18;
    //     }
    // }

    //     updateMaxTextLength();
        
    //     window.addEventListener('resize', updateMaxTextLength);
        
       
        

    
});









$(document).ready(function () {
    const selectedItems = new Map();
    const maxSelectedItems = 5;
    const deleteAnimationDuration = 200; // 動畫持續時間，單位是毫秒
    let totalStayTime = 0;

    // 監聽選擇項目的變化，根據情況啟用或禁用送出按鈕
    function updateSubmitButtonStatus() {


        // 檢查選擇項目的數量和總停留時間
        if (selectedItems.size < 3 || totalStayTime > 480) {
            $('#SubmitButton').prop('disabled', true);
        } else {
            $('#SubmitButton').prop('disabled', false);
        }


        if (selectedItems.size < 3) {
            $('.hint-word').text('請選擇3~5個景點!'); // 顯示 .hint-word 區塊並設置文本
            $('.hint-word').show();
        } else if (selectedItems.size > 2) {
            $('.hint-word').text('最多選擇5個景點!'); // 顯示 .hint-word 區塊並設置文本
            $('.hint-word').show();
        } else {
            $('.hint-word').hide(); // 隱藏 .hint-word 區塊
        }

        if (totalStayTime <= 480) {
            $('.notification').hide();
            $('#totalStayTime').show();
        } else {
            $('.notification').show();
            $('#totalStayTime').hide();
        }
    }

    function updateSelectedItemsArray() {
        const selectedItemsArray = Array.from(selectedItems.values());
    }

    $('.lightbox-content').on('click', '.data-item', function () {
        const itemId = $(this).data('id');
        if (!selectedItems.has(itemId)) {
            if (selectedItems.size < maxSelectedItems) {
                selectedItems.set(itemId, $(this).text());

                //獲取所選擇的選項的建議停留時間
                const stayTime = parseInt($(this).find('.point-text').text().match(/推薦停留時間：(\d+) 分鐘/)[1]);
                //移動時間
                const moveTime = 30;

                //加總
                totalStayTime += stayTime + moveTime;


                // 更改所選項目的顏色
                $(this).addClass('selected');


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

                //更新停留總時間
                $('#totalStayTime').text(`總停留時間：${totalStayTime} 分鐘`);
                // 檢查總停留時間是否超過480分鐘，並啟用或禁用送出按鈕
                updateSubmitButtonStatus();

            }
        }
    });


    // 監聽取消按鈕的點擊事件
    // 在選中項目被刪除時，同時更新保存所選項目值的陣列
    $(document).on('click', '.cancel-button', function () {
        const canceledItemId = $(this).parent().data('id');
        const canceledItemElement = $(this).parent();
        const stayTime = parseInt($('.lightbox-content .data-item[data-id="' + canceledItemId + '"]').find('.point-text').text().match(/推薦停留時間：(\d+) 分鐘/)[1]);


        // 顯示自訂對話框
        const dialog = document.getElementById('custom-dialog1');
        dialog.style.display = 'flex';

        // 確定按鈕的點擊事件
        $(document).off('click', '#confirm-yes'); // 解除舊的事件綁定
        $(document).on('click', '#confirm-yes', function () {
            selectedItems.delete(canceledItemId); // 使用 Map 的 delete 方法來移除項目

            // 移除所選項目的顏色
            $('.lightbox-content .data-item[data-id="' + canceledItemId + '"]').removeClass('selected');

            const moveTime = 30;
            totalStayTime -= stayTime + moveTime;
            //更新總停留時間
            $('#totalStayTime').text(`總停留時間：${totalStayTime} 分鐘`);
            updateSubmitButtonStatus();

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
        $(document).off('click', '#confirm-no'); // 解除舊的事件綁定
        $(document).on('click', '#confirm-no', function () {
            dialog.style.display = 'none'; // 隱藏對話框

            // 解除取消按鈕的點擊事件，避免多次綁定
            $(document).off('click', '#confirm-no');
        });



    });






    // 送出按鈕點擊事件
    const fakeBackendEndpoint = '/route';//指定後端端點
    // const fakeBackendEndpoint = '/fake-backend-endpoint';//指定後端端點
    // $('#SubmitButton').click(async (event) => {

    //     const overlay = document.getElementById('overlay');

    //     overlay.style.display = 'flex'; 
        
    //     const selectedItemsArray = Array.from(selectedItems.values());
    //     try {
    //         // const response = await fetch('/fake-backend-endpoint', {
    //         const response = await fetch('/route', {
    //             method: 'POST',
    //             headers: {
    //                 'Content-Type': 'application/json'
    //             },
    //             //指定HTTP請求或回應中包含的數據的類型。
    //             body: JSON.stringify({ selectedItems: selectedItemsArray })
    //         });

        
    //     } catch (error) {
    //         console.error(error);
          
    //     } finally {
           
    //     }

    // });
    $('#SubmitButton').click((event) => {
        const selectedItemsArray = Array.from(selectedItems.values());
        document.getElementById('selectedItemsInput').value = JSON.stringify({ selectedItems: selectedItemsArray });
    });

});




var backButton = document.getElementById("BackButton");
var customDialog = document.getElementById("custom-dialog2");
var confirmButton = document.getElementById("confirm-yes2");
var cancelButton = document.getElementById("confirm-no2");

backButton.addEventListener("click", function () {

    customDialog.style.display = "flex";
});
//確定
confirmButton.addEventListener("click", function () {
    history.back();

    customDialog.style.display = "none";
});
//取消
cancelButton.addEventListener("click", function () {
    customDialog.style.display = "none";
});