(function ($) {
    $(function () {
        var selectLevel = $("select[name=level]");
        var searchInput = $("input[type=text][class=search]");
        var targetTable = $("table.filtered.online tbody");
        var targetRows = $("table.filtered.online tr:not('.header')");

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
            var level = selectLevel.val();
            var searchText = (searchInput.val() || "").toUpperCase();
            if (level || searchText) {
                targetRows.each(function (i, el) {
                    var visible = true;
                    if (level) {
                        var label = selectLevel.find("option:selected").text();
                        let rowLevel = $(el).find("td.level").text();
                        visible = visible && rowLevel === label;
                    }

                    if (searchText && visible) {
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

        selectLevel.on("change", filterTable);
        searchInput.on("keyup", delay(filterTable));
        $("#clear").on("click", function () {
            console.log("Clearing logs");
            $.ajax({
                url: "./?page=clear", success: function () {
                    fetch();
                }
            });
        });

        function fetch() {
            console.log("Fetching logs");
            $.ajax({
                url: "./?page=logs",
                method: "GET",
                success: function (risposta) {
                    targetTable.html("");
                    $(risposta).each(function (index, item) {
                        targetTable.prepend(
                            "<tr><td>" + (index + 1) +
                            "</td><td>" + item.created +
                            "</td><td>" + item.levelname +
                            "</td><td>" + item.name +
                            "</td><td>" + item.message +
                            "</td><td>" + item.msg +
                            "</td></tr>"
                        );
                    });
                },
                error: function () {
                    console.log("Si è verificato un errore");
                }
            });
        }

        setInterval(fetch, 5000);
        filterTable();
        fetch();
    });
})($);
