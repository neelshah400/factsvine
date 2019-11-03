// url = window.location.href;
// page = url.substring(url.lastIndexOf('/')).substring(1)
// if (page === 'feed') {
//     headlines = Array();
//     summaries = Array();
//     for (var i = 0; i < 5; i++) {
//         headlines[i] = document.getElementById("h" + i + "").value;
//         summaries[i] = document.getElementById("s" + i + "").value;
//     }
//     for (var i = 0; i < headlines.length; i++) {
//         document.getElementById("cards").innerHTML +=
//         '   <div class="card">' + 
//         '       <div class="card-body">' + 
//         '           <h5 class="card-title">' + headlines[i] + '</h5>' +
//         '           <p class="card-text">' + summaries[i] + '</p>' +
//         '       </div>' +
//         '   </div>';
//     }
// }