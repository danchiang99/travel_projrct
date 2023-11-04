// 側邊面板
const menuButton = document.getElementById("hamburger-btn");
const sidebar = document.getElementById("sidebar");
let isSidebarOpen = false;

function toggleSidebar() {
    if (window.matchMedia("(max-width: 450px)").matches) {
        sidebar.style.width = (sidebar.style.width === "100vw") ? "0" : "100vw";
    } else {
        sidebar.style.width = (sidebar.style.width === "190px") ? "0" : "190px";
    }
}

function applyResponsiveEffect() {
    menuButton.removeEventListener("click", toggleSidebar);
    menuButton.addEventListener("click", toggleSidebar);

}

// 頁面載入完成時套用一次效果
applyResponsiveEffect();

// 監聽視窗大小變化，套用適當的效果
window.addEventListener('resize', applyResponsiveEffect);

// 選項點擊時的處理
const dropdownItems = document.querySelectorAll(".dropdown-item");


//這行以下還有問題！！！
// dropdownItems.forEach(item => {
//     item.addEventListener("click", function (event) {
//         event.preventDefault();
//         const value = this.textContent;
//         console.log("選擇的值:", value);
//     });
// });

// // 點擊選擇框時顯示選單
// const dropdownToggle = document.querySelector(".dropdown-toggle");
// const dropdownContent = document.querySelector(".dropdown-content");

// dropdownToggle.addEventListener("click", function () {
//     dropdownContent.classList.toggle("show");
// });

// // 在選單外點擊時隱藏選單
// document.addEventListener("click", function (event) {
//     if (!dropdownToggle.contains(event.target) && !dropdownContent.contains(event.target)) {
//         dropdownContent.classList.remove("show");
//     }
// });


// //回景點類型選擇頁
// document.addEventListener("DOMContentLoaded", function () {

//     var myLink = document.querySelectorAll(".menu_item");
//     var leaveDialog = document.getElementById("leave-dialog");
//     var yesButton = document.getElementById("leave-yes");
//     var noButton = document.getElementById("leave-no");


//     myLink.forEach(function (myLink) {
//         myLink.addEventListener("click", function (event) {

//             event.preventDefault();


//             leaveDialog.style.display = "block";
//         });
//     });

//     yesButton.addEventListener("click", function () {

//         var linkURL = myLink.getAttribute("href");
//         window.location.href = linkURL;

//         leaveDialog.style.display = "none";
//     });

//     noButton.addEventListener("click", function () {

//         leaveDialog.style.display = "none";
//     });

// });






