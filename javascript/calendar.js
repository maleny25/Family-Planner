// var cal = {
//   /* [PROPERTIES] */
//   mName : ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], // Month Names
//   data : null, // Events for the selected period
//   sDay : 0, // Current selected day
//   sMth : 0, // Current selected month
//   sYear : 0, // Current selected year
//   sMon : false, // Week start on Monday?
//
//   /* [FUNCTIONS] */
//   list : function () {
//   // cal.list() : draw the calendar for the given month
//
//     // BASIC CALCULATIONS
//     // Note - Jan is 0 & Dec is 11 in JS.
//     // Note - Sun is 0 & Sat is 6
//     cal.sMth = parseInt(document.getElementById("cal-mth").value); // selected month
//     cal.sYear = parseInt(document.getElementById("cal-yr").value); // selected year
//     var daysInMth = new Date(cal.sYear, cal.sMth+1, 0).getDate(), // number of days in selected month
//         startDay = new Date(cal.sYear, cal.sMth, 1).getDay(), // first day of the month
//         endDay = new Date(cal.sYear, cal.sMth, daysInMth).getDay(); // last day of the month
//
//     // LOAD DATA FROM LOCALSTORAGE(change)
//     cal.data = localStorage.getItem("cal-" + cal.sMth + "-" + cal.sYear);
//     if (cal.data==null) {
//       localStorage.setItem("cal-" + cal.sMth + "-" + cal.sYear, "{}");
//       cal.data = {};
//     } else {
//       cal.data = JSON.parse(cal.data);
//     }
//
//     // DRAWING CALCULATIONS
//     // Determine the number of blank squares before start of month
//     var squares = [];
//     if (cal.sMon && startDay != 1) {
//       var blanks = startDay==0 ? 7 : startDay ;
//       for (var i=1; i<blanks; i++) { squares.push("b"); }
//     }
//     if (!cal.sMon && startDay != 0) {
//       for (var i=0; i<startDay; i++) { squares.push("b"); }
//     }
//
//     // Populate the days of the month
//     for (var i=1; i<=daysInMth; i++) { squares.push(i); }
//
//     // Determine the number of blank squares after end of month
//     if (cal.sMon && endDay != 0) {
//       var blanks = endDay==6 ? 1 : 7-endDay;
//       for (var i=0; i<blanks; i++) { squares.push("b"); }
//     }
//     if (!cal.sMon && endDay != 6) {
//       var blanks = endDay==0 ? 6 : 6-endDay;
//       for (var i=0; i<blanks; i++) { squares.push("b"); }
//     }
//
//     // DRAW HTML
//     // Container & Table
//     var container = document.getElementById("cal-container"),
//         cTable = document.createElement("table");
//     cTable.id = "calendar";
//     container.innerHTML = "";
//     container.appendChild(cTable);
//
//     // First row - Days
//     var cRow = document.createElement("tr"),
//         cCell = null,
//         days = ["Sun", "Mon", "Tue", "Wed", "Thur", "Fri", "Sat"];
//     if (cal.sMon) { days.push(days.shift()); }
//     for (var d of days) {
//       cCell = document.createElement("td");
//       cCell.innerHTML = d;
//       cRow.appendChild(cCell);
//     }
//     cRow.classList.add("head");
//     cTable.appendChild(cRow);
//
//     // Days in Month
//     var total = squares.length;
//     cRow = document.createElement("tr");
//     cRow.classList.add("day");
//     for (var i=0; i<total; i++) {
//       cCell = document.createElement("td");
//       if (squares[i]=="b") { cCell.classList.add("blank"); }
//       else {
//         cCell.innerHTML = "<div class='dd'>"+squares[i]+"</div>";
//         if (cal.data[squares[i]]) {
//           cCell.innerHTML += "<div class='evt'>" + cal.data[squares[i]] + "</div>";
//         }
//         cCell.addEventListener("click", function(){
//           cal.show(this);
//         });
//       }
//       cRow.appendChild(cCell);
//       if (i!=0 && (i+1)%7==0) {
//         cTable.appendChild(cRow);
//         cRow = document.createElement("tr");
//         cRow.classList.add("day");
//       }
//     }
//
//     // REMOVE ANY ADD/EDIT EVENT DOCKET
//     // cal.close();
//   },
//   //
//   // show : function (el) {
//   // // cal.show() : show edit event docket for selected day
//   // // PARAM el : Reference back to cell clicked
//   //
//   //   // FETCH EXISTING DATA
//   //   cal.sDay = el.getElementsByClassName("dd")[0].innerHTML;
//   //
//   //   // DRAW FORM
//   //   var tForm = "<h1>" + (cal.data[cal.sDay] ? "EDIT" : "ADD") + " EVENT</h1>";
//   //   tForm += "<div id='evt-date'>" + cal.sDay + " " + cal.mName[cal.sMth] + " " + cal.sYear + "</div>";
//   //   tForm += "<textarea id='evt-details' required>" + (cal.data[cal.sDay] ? cal.data[cal.sDay] : "") + "</textarea>";
//   //   tForm += "<input type='button' value='Close' onclick='cal.close()'/>";
//   //   tForm += "<input type='button' value='Delete' onclick='cal.del()'/>";
//   //   tForm += "<input type='submit' value='Save'/>";
//   //
//   //   // ATTACH
//   //   var eForm = document.createElement("form");
//   //   eForm.addEventListener("submit", cal.save);
//   //   eForm.innerHTML = tForm;
//   //   var container = document.getElementById("cal-event");
//   //   container.innerHTML = "";
//   //   container.appendChild(eForm);
//   // },
//   //
//   // close : function () {
//   // // cal.close() : close event docket
//   //
//   //   document.getElementById("cal-event").innerHTML = "";
//   // },
//   //
//   // save : function (evt) {
//   // // cal.save() : save event
//   //
//   //   evt.stopPropagation();
//   //   evt.preventDefault();
//   //   cal.data[cal.sDay] = document.getElementById("evt-details").value;
//   //   localStorage.setItem("cal-" + cal.sMth + "-" + cal.sYear, JSON.stringify(cal.data));
//   //   cal.list();
//   // },
//   //
//   // del : function () {
//   // // cal.del() : Delete event for selected date
//   //
//   //   if (confirm("Remove event?")) {
//   //     delete cal.data[cal.sDay];
//   //     localStorage.setItem("cal-" + cal.sMth + "-" + cal.sYear, JSON.stringify(cal.data));
//   //     cal.list();
//   //   }
//   // }
// };
//
// // INIT - DRAW MONTH & YEAR SELECTOR
// window.addEventListener("load", function () {
//   // DATE NOW
//   var now = new Date(),
//       nowMth = now.getMonth(),
//       nowYear = parseInt(now.getFullYear());
//
//   // APPEND MONTHS SELECTOR
//   var month = document.getElementById("cal-mth");
//   for (var i = 0; i < 12; i++) {
//     var opt = document.createElement("option");
//     opt.value = i;
//     opt.innerHTML = cal.mName[i];
//     if (i==nowMth) { opt.selected = true; }
//     month.appendChild(opt);
//   }
//
//   // APPEND YEARS SELECTOR
//   // Set to 10 years range. Change this as you like.
//   var year = document.getElementById("cal-yr");
//   for (var i = nowYear-10; i<=nowYear+10; i++) {
//     var opt = document.createElement("option");
//     opt.value = i;
//     opt.innerHTML = i;
//     if (i==nowYear) { opt.selected = true; }
//     year.appendChild(opt);
//   }
//
//
//   // START - DRAW CALENDAR
//   document.getElementById("cal-set").addEventListener("click", cal.list);
//   cal.list();
// });

var cal1 = {
  moName : ["null","Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], // Month Names
  data : null, // Events for the selected period
  seMon : false,
  seDay : 0, // Current selected day
  seMth : 0, // Current selected month
  seYear : 0,

  list2 : function () {
    cal1.seMth = parseInt(document.getElementById("cal1-mth").value); // selected month
    cal1.seYear = parseInt(document.getElementById("cal1-yr").value);
    cal1.seDay = parseInt(document.getElementById("cal1-day").value);
    // var daysInMth1 = new Date(cal1.seYear, cal1.seMth+1, 0).getDate(), // number of days in selected month
    //     startDay1 = new Date(cal1.seYear, cal1.seMth, 1).getDay(), // first day of the month
    //     endDay1 = new Date(cal1.seYear, cal1.seMth, daysInMth).getDay();

    cal1.data = localStorage.getItem("cal1-" + cal1.seMth + "-" + cal1.seYear);
    if (cal1.data==null) {
      localStorage.setItem("cal1-" + cal1.seMth + "-" + cal1.seYear, "{}");
      cal1.data = {};
    } else {
      cal1.data = JSON.parse(cal1.data);
    }

  }}

window.addEventListener("load",  function () {

    var daysInMth1 = new Date(cal1.seYear, cal1.seMth+1, 0).getDate(), // number of days in selected month
        startDay1 = new Date(cal1.seYear, cal1.seMth, 1).getDay(), // first day of the month
        endDay1 = new Date(cal1.seYear, cal1.seMth, daysInMth1).getDay();

      // DATE NOW
    var now1 = new Date(),
        nowMth1 = now1.getMonth(),
        nowDay1 = parseInt(now1.getDay()),
        nowYear1 = parseInt(now1.getFullYear());

      // APPEND MONTHS SELECTOR
    var month1 = document.getElementById("cal1-mth");
    for (var i = 1; i < 13; i++) {
      var opt1 = document.createElement("option");
      opt1.value = i;
      opt1.innerHTML = cal1.moName[i];
      if (i==nowMth1) { opt1.selected = true; }
      month1.appendChild(opt1);
    }

      // APPEND YEARS SELECTOR
      // Set to 10 years range. Change this as you like.
    var year1 = document.getElementById("cal1-yr");
    for (var i = nowYear1-10; i<=nowYear1+10; i++) {
      var opt1 = document.createElement("option");
      opt1.value = i;
      opt1.innerHTML = i;
      if (i==nowYear1) { opt1.selected = true; }
      year1.appendChild(opt1);
    }

    var day1 = document.getElementById("cal1-day");
    for (var i = 1; i<=31; i++) {
      var opt1 = document.createElement("option");
      opt1.value = i;
      opt1.innerHTML = i;
      if (i==nowDay1) { opt1.selected = true; }
      day1.appendChild(opt1);
    }



});

var cal2 = {
  monName : ["null","Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], // Month Names
  data : null, // Events for the selected period
  secMon : false,
  secDay : 0, // Current selected day
  secMth : 0, // Current selected month
  secYear : 0,

  list3 : function () {
    cal2.secMth = parseInt(document.getElementById("cal2-mth").value); // selected month
    cal2.secYear = parseInt(document.getElementById("cal2-yr").value);
    cal2.secDay = parseInt(document.getElementById("cal2-day").value);
    // var daysInMth1 = new Date(cal1.seYear, cal1.seMth+1, 0).getDate(), // number of days in selected month
    //     startDay1 = new Date(cal1.seYear, cal1.seMth, 1).getDay(), // first day of the month
    //     endDay1 = new Date(cal1.seYear, cal1.seMth, daysInMth).getDay();

    cal2.data = localStorage.getItem("cal2-" + cal2.secMth + "-" + cal2.secYear);
    if (cal2.data==null) {
      localStorage.setItem("cal2-" + cal2.secMth + "-" + cal2.secYear, "{}");
      cal2.data = {};
    } else {
      cal2.data = JSON.parse(cal2.data);
    }

  }}

window.addEventListener("load",  function () {

    var daysInMth2 = new Date(cal2.secYear, cal2.secMth+1, 0).getDate(), // number of days in selected month
        startDay2 = new Date(cal2.secYear, cal2.secMth, 1).getDay(), // first day of the month
        endDay2 = new Date(cal2.secYear, cal2.secMth, daysInMth2).getDay();

      // DATE NOW
    var now2 = new Date(),
        nowMth2 = now2.getMonth(),
        nowDay2 = parseInt(now2.getDay()),
        nowYear2 = parseInt(now2.getFullYear());

      // APPEND MONTHS SELECTOR
    var month2 = document.getElementById("cal2-mth");
    for (var i = 1; i < 13; i++) {
      var opt2 = document.createElement("option");
      opt2.value = i;
      opt2.innerHTML = cal2.monName[i];
      if (i==nowMth2) { opt2.selected = true; }
      month2.appendChild(opt2);
    }

      // APPEND YEARS SELECTOR
      // Set to 10 years range. Change this as you like.
    var year2 = document.getElementById("cal2-yr");
    for (var i = nowYear2-10; i<=nowYear2+10; i++) {
      var opt2 = document.createElement("option");
      opt2.value = i;
      opt2.innerHTML = i;
      if (i==nowYear2) { opt2.selected = true; }
      year2.appendChild(opt2);
    }

    var day2 = document.getElementById("cal2-day");
    for (var i = 1; i<=31; i++) {
      var opt2 = document.createElement("option");
      opt2.value = i;
      opt2.innerHTML = i;
      if (i==nowDay2) { opt2.selected = true; }
      day2.appendChild(opt2);
    }



});
