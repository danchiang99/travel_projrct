
//回上一頁
document.addEventListener("DOMContentLoaded", function () {

    var backButton = document.getElementById("BackButton2");
    var customDialog = document.getElementById("custom-dialog3");
    var confirmButton = document.getElementById("confirm-yes3");
    var cancelButton = document.getElementById("confirm-no3");

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
});


    document.addEventListener("DOMContentLoaded", function () {
//回首頁


    var homeButton = document.getElementById("HomeButton");
    var customDialog = document.getElementById("custom-dialog4");
    var confirmButton = document.getElementById("confirm-yes4");
    var cancelButton = document.getElementById("confirm-no4");

    homeButton.addEventListener("click", function () {

        customDialog.style.display = "flex";
    });
    //確定
    confirmButton.addEventListener("click", function () {
       
        customDialog.style.display = "none";
        window.location.href = "/";
       
    });
    //取消
    cancelButton.addEventListener("click", function () {
        customDialog.style.display = "none";
    });


});




window.onload = function() {
    initMap(); // 當網頁完全載入後執行initMap函數
};

function initMap() {
    const map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: originLat, lng: originLng },
        zoom: 13,
    });

    const directionsService = new google.maps.DirectionsService();
    const directionsRenderer = new google.maps.DirectionsRenderer({
        map: map,
    });

    const origin = { lat: originLat, lng: originLng };
    const destination = { lat: destinationLat, lng: destinationLng };
    const waypoints = [];

    for (let i = 0; i < waypointsData.length; i++) {
        waypoints.push({ location: { lat: waypointsData[i].latitude, lng: waypointsData[i].longitude } });
    }

    const request = {
        origin: origin,
        destination: destination,
        waypoints: waypoints,
        travelMode: google.maps.TravelMode.DRIVING,
    };

    directionsService.route(request, function (result, status) {
        if (status == google.maps.DirectionsStatus.OK) {
            directionsRenderer.setDirections(result);
        }
    });
}


// 獲取所有具有 .point-title 類別的元素
var pointTitles = document.querySelectorAll(".point-title");

// 遍歷所有 .point-title 元素
pointTitles.forEach(function(pointTitle, index) {
    // 獲取元素的文本內容
    var title = pointTitle.textContent;

    // 檢查文本內容是否為 "午餐" 或 "晚餐"
    if (title === "午餐" || title === "晚餐") {
        // 如果是午餐或晚餐，找到相應的 元素並設定高度顏色
        var parentItineraryItem = pointTitle.closest(".itinerary-item");
        var pointTitleElement = parentItineraryItem.querySelector(".point-title");
        if (pointTitleElement) {
            pointTitleElement.classList.add("lunch-dinner");
        }

        if (parentItineraryItem) {

            if (window.matchMedia("(max-width: 450px)").matches) {
                parentItineraryItem.style.height = "40px";
            } else {
                parentItineraryItem.style.height = "45px";
            }


        }
      // 隱藏 .arrival 和 .end-time 元素
      var arrivalElement = parentItineraryItem.querySelector(".arrival");
      var endTimeElement = parentItineraryItem.querySelector(".end-time");
      if (arrivalElement) {
          arrivalElement.style.display = "none";
      }
      if (endTimeElement) {
          endTimeElement.style.display = "none";
      }
      // 更改 .point-text 文字
      var pointTextElement = parentItineraryItem.querySelector(".point-text");
      if (pointTextElement) {
          pointTextElement.textContent = "～"; // 更改成您想要的文字
      }


         // 隱藏目前位置的上一個 leg 元素
         if (index > 0) {
            var previousItineraryItem = pointTitles[index - 1].closest(".itinerary-item");
            var previousLegElement = previousItineraryItem.querySelector(".leg");
            if (previousLegElement) {
                previousLegElement.style.display = "none";
            }
        }
    }
    
    const pointTitleElements = document.querySelectorAll('.point-title');
    
    
    const maxTextLength = 19;
    
    
    pointTitleElements.forEach((element) => {
    const text = element.textContent;
    if (text.length > maxTextLength) {
    
        const truncatedText = text.slice(0, maxTextLength) + '…';
        element.textContent = truncatedText;
    }
    });
    
});


