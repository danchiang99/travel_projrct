$(document).ready(function () {
    const content = $('.lightbox-content');
    const prevBtn = $('.prev-btn');
    const nextBtn = $('.next-btn');
    const itemWidth = $('.member').outerWidth(true);
    const itemsPerPage = 1; //每頁顯示1
    const totalItems = $('.member').length - 1;
    const totalPages = totalItems; // 每個項目為一頁
    let currentPage = 0;

    function updateContentPosition() {
        const newPosition = -currentPage * itemWidth * itemsPerPage;
        content.css('transform', `translateX(${newPosition}px)`);
    }

    prevBtn.on('click', function () {
        if (currentPage > 0) {
            currentPage--;
            updateContentPosition();
        } else {
            currentPage = totalPages; // 到最後一頁時跳回第一頁
            updateContentPosition();
        }
    });

    nextBtn.on('click', function () {
        if (currentPage < totalPages) {
            currentPage++;
            updateContentPosition();
        } else {
            currentPage = 0; // 到最後一頁時跳回第一頁
            updateContentPosition();
        }
    });

    //先關掉最後再打開
    setInterval(function () {
        if (currentPage < totalPages) {
            currentPage++;
            updateContentPosition();
        } else {
            currentPage = 0;
            updateContentPosition();
        }
    }, 10000);


    updateContentPosition();
});