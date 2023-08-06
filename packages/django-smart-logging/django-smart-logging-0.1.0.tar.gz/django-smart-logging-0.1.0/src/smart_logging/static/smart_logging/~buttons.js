(function ($) {
    $(function () {
        $("a.toggler").on("click", function () {
            $("div.logging.panel").removeClass("active");
            $("a.button.logging.toggler").removeClass("selected");
            $(this).addClass("selected");
            $($(this).data("toggler")).addClass("active");
        });
    });
})($);
