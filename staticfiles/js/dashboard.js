   /* Kristuff.WebUI.SideMenu */
   (function (window, undefined) {
    "use strict";
    // responsive pinnable sidemenu component
    var sideMenu = function (el) {
        var htmlSideMenu = el,
            htmlSideMenuPinTrigger = {},
            htmlSideMenuPinTriggerImage = {},
            htmlOverlay = {};

        var init = function () {
            // htmlSideMenuPinTrigger = el.querySelector(
            //   ".wui-side-menu-pin-trigger"
            // );
            htmlSideMenuPinTriggerImage =
                //   htmlSideMenuPinTrigger.querySelector("i.fa");
                htmlOverlay = document.querySelector(".wui-overlay");

            Array.prototype.forEach.call(
                document.querySelectorAll(".wui-side-menu-trigger"),
                function (elmt, i) {
                    elmt.addEventListener(
                        "click",
                        function (e) {
                            e.preventDefault();
                            toggleMenuState();
                        },
                        false
                    );
                }
            );

            // htmlSideMenuPinTrigger.addEventListener(
            //   "click",
            //   function (e) {
            //     e.preventDefault();
            //     toggleMenuPinState();
            //   },
            //   false
            // );

            htmlOverlay.addEventListener(
                "click",
                function (e) {
                    htmlSideMenu.classList.remove("open");
                },
                false
            );
            window.addEventListener("resize", checkIfNeedToCloseMenu, false);
            checkIfNeedToCloseMenu();
        };

        var toggleMenuState = function () {
            htmlSideMenu.classList.toggle("open");
            // menuStateChanged(
            //   htmlSideMenu,
            //   htmlSideMenu.classList.contains("open")
            // );
        };
        var toggleMenuPinState = function () {
            htmlSideMenu.classList.toggle("pinned");
            htmlSideMenuPinTriggerImage.classList.toggle("fa-rotate-90");
            if (htmlSideMenu.classList.contains("pinned") !== true) {
                htmlSideMenu.classList.remove("open");
            }
            menuPinStateChanged(
                htmlSideMenu,
                htmlSideMenu.classList.contains("pinned")
            );
        };

        var checkIfNeedToCloseMenu = function () {
            var width =
                window.innerWidth ||
                document.documentElement.clientWidth ||
                document.body.clientWidth;
            if (
                width <= 767 &&
                htmlSideMenu.classList.contains("open") === true
            ) {
                htmlSideMenu.classList.remove("open");
                menuStateChanged(
                    htmlSideMenu,
                    htmlSideMenu.classList.contains("open")
                );
            }
            if (
                width > 767 &&
                htmlSideMenu.classList.contains("pinned") === false
            ) {
                htmlSideMenu.classList.remove("open");
                menuStateChanged(
                    htmlSideMenu,
                    htmlSideMenu.classList.contains("open")
                );
            }
        };
        //   var menuStateChanged = function (element, state) {
        //     var evt = new CustomEvent("menuStateChanged", {
        //       detail: { open: state },
        //     });
        //     element.dispatchEvent(evt);
        //   };

        var menuPinStateChanged = function (element, state) {
            var evt = new CustomEvent("menuPinStateChanged", {
                detail: {
                    pinned: state
                },
            });
            element.dispatchEvent(evt);
        };
        init();
        return {
            htmlElement: htmlSideMenu,
            toggleMenuState: toggleMenuState,
            toggleMenuPinState: toggleMenuPinState,
        };
    };

    window.SideMenu = sideMenu;
})(window);

var documentReady = function (fn) {
    if (document.readyState != "loading") {
        fn();
    } else {
        document.addEventListener("DOMContentLoaded", fn);
    }
};

documentReady(function () {
    var sample = new SideMenu(document.querySelector(".wui-side-menu"));
    sample.htmlElement.addEventListener(
        "menuPinStateChanged",
        function (e) {
            // document.querySelector("#events").innerHTML +=
            "menuPinStateChanged , menu pinned? => " + e.detail.pinned + "<br>";
        },
        false
    );

    sample.htmlElement.addEventListener(
        "menuStateChanged",
        function (e) {
            document.querySelector("#events").innerHTML +=
                "menuStateChanged , menu open? => " + e.detail.open + "<br>";
        },
        false
    );
});












$(document).ready(function(){
	$('a[href="#search"]').on('click', function(event) {                    
		$('#search').addClass('open');
		$('#search > form > input[type="search"]').focus();
	});            
	$('#search, #search button.close').on('click keyup', function(event) {
		if (event.target == this || event.target.className == 'close' || event.keyCode == 27) {
			$(this).removeClass('open');
		}
	});            
});