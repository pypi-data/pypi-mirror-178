(function ($) {
    $(function () {
        var searchInput = $("input[type=text][class=search]");
        // var targetTable = $("table.filtered tbody");
        var targetRows = $("table.filtered tr:not('.header')");

        function delay(callback, ms) {
            var timer = 0;
            return function () {
                var context = this, args = arguments;
                clearTimeout(timer);
                timer = setTimeout(function () {
                    callback.apply(context, args);
                }, ms || 0);
            };
        }

        function filterTable() {
            var searchText = (searchInput.val() || "").toUpperCase();
            if (searchText) {
                targetRows.each(function (i, el) {
                    var visible = true;
                    if (searchText) {
                        let rowLogger = $(el).find("td.search").text().toUpperCase();
                        visible = visible && (rowLogger.toUpperCase().indexOf(searchText) > -1);
                    }
                    if (visible) {
                        $(el).show();
                    } else {
                        $(el).hide();
                    }
                });
            } else {
                $("table.filtered tr:not('.header')").show();
            }
        }
        searchInput.on("keyup", delay(filterTable));

        filterTable();
    });
})($);
