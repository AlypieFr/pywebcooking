if (!panel) {
    throw "panel was not included!"
}

panel.recipes = {};

panel.recipes.init = function () {
    panel.recipes.init_events();
};

panel.recipes.init_events = function () {
    $("div.list-recipes table thead tr th:first-child input[type=checkbox], div.list-recipes table tfoot tr th:first-child input[type=checkbox]").click(function () {
        panel.recipes.check_all(this.checked);
    });
};

panel.recipes.check_all = function (check) {
    $("div.list-recipes table tr td:first-child input[type=checkbox]," +
        "div.list-recipes table tr th:first-child input[type=checkbox]").prop("checked", check);
};