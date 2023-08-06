(function ($) {
    $(function () {
        var selectLevel = $("select[name=level]");
        var selectHandler = $("select[name=handler]");
        var searchInput = $("input[type=text][class=search]");
        var checkPropagate = $("select[name=propagate]");
        var inputs = $("table :input");
        var targetRows = $("table.filtered.config tr:not('.header')");

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
            var handler = selectHandler.val();
            var searchText = (searchInput.val() || "").toUpperCase();
            var propagate = checkPropagate.val();
            if (level || handler || searchText || propagate) {
                targetRows.each(function (i, el) {
                    var visible = true;
                    if (level) {
                        let rowLevel = $(el).find("td.level select").val();
                        visible = visible && rowLevel === level;
                    }

                    if (visible && propagate !== "") {
                        let rowValue = $(el).find("td.propagate input[type=checkbox]:checked").length > 0;
                        if (propagate === "-1") {
                            visible = rowValue;
                        } else if (propagate === "0") {
                            visible = !rowValue;
                        } else {
                            visible = false;
                        }
                    }
                    if (searchText && visible) {
                        let rowLogger = $(el).find("td.search").text().toUpperCase();
                        visible = visible && (rowLogger.toUpperCase().indexOf(searchText) > -1);
                    }
                    if (handler && visible) {
                        if (handler === "0") { // Any Handler
                            visible = $(el).find("td.handlers input[type=checkbox]:checked").length > 0;
                        } else if (handler === "-1") { // No handlers
                            visible = $(el).find("td.handlers input[type=checkbox]:checked").length === 0;
                        } else {
                            var rv = false;
                            $(el).find("td.handlers input[type=checkbox]:checked").each(function (i, e) {
                                rv = false;
                                if (!rv && handler === $(e).val()) {
                                    rv = true;
                                }
                            });
                            visible = rv;
                        }
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
        selectHandler.on("change", filterTable);
        checkPropagate.on("change", delay(filterTable));
        searchInput.on("keyup", delay(filterTable));

        $("td.undo").on("click", function () {
            var $row = $(this).parents("tr.row");
            $row.find(":input").each(function () {
                if ($(this).is("input[type=checkbox]")) {
                    $(this).prop("checked", $(this).data("val"));
                } else if ($(this).is("select")) {
                    $(this).val($(this).data("val"));
                }
            });
            $row.data("changes", []);
            $row.removeClass("changed");
        });

        $("table tr").each(function (index, value) {
            $(this).data("changes", []);
        });

        inputs.each(function (index, value) {
            if ($(this).is("input[type=checkbox]")) {
                $(this).data("val", $(this).is(":checked"));
            } else if ($(this).is("select")) {
                $(this).data("val", $(this).val());
            }
        }).on("change", function (e) {
            var $row = $(this).parents("tr.row");
            var changes = $row.data("changes");
            var changed = false;
            if ($(this).is("input[type=checkbox]")) {
                changed = $(this).is(":checked") !== $(this).data("val");
            } else if ($(this).is("select")) {
                changed = $(this).val() !== $(this).data("val");
            }
            if (changed) {
                changes.push($(this));
            } else {
                changes.pop();
            }
            if (changes.length > 0) {
                $row.addClass("changed");
            } else {
                $row.removeClass("changed");
            }
            $row.data("changes", changes);
        });
        filterTable();
    });
})($);
