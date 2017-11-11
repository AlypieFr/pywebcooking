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
    $("div.form-apply-recipes form.grouped-actions").submit(function(e) {
        e.preventDefault();
        panel.recipes.submit_grouped_actions(parseInt($(this).find("select").val()));
    });
    $("div.form-apply-recipes form#sel-filters").submit(function(e) {
        e.preventDefault();
        panel.recipes.submit_filter_form();
    });
    $("button#empty-trash").click(panel.recipes.empty_trash);
    let list_recipes = $("div.list-recipes");
    list_recipes.find("table").find("tr").mouseover(function() {
        $(this).find(".actions-a-recipe").show();
    });
    list_recipes.find("table").find("tr").mouseout(function() {
        $(this).find(".actions-a-recipe").hide();
    });
};

panel.recipes.check_all = function (check) {
    $("div.list-recipes table tr td:first-child input[type=checkbox]," +
        "div.list-recipes table tr th:first-child input[type=checkbox]").prop("checked", check);
};

panel.recipes.submit_grouped_actions = function (action) {
    if (action === 0) {
        alert(django.gettext("Please select an action to do!"))
    }
    else {
        // Get selected recipes:
        let selection = $("div.list-recipes table tbody tr td:first-child input[type=checkbox]:checked");
        let selected = [];
        selection.each(function () {
            selected.push(parseInt(this.value));
        });
        $.post("/panel/" + django.gettext("recipes") + "/change/",
            {
                selection: selected,
                action: action,
                csrfmiddlewaretoken: panel.csrftoken
            },
            function(data, status) {
                if (data["success"]) {
                    location.reload();
                }
                else {
                    alert("message" in data ? data["message"] : "An error has occurred!")
                }
            })
    }
};

panel.recipes.submit_filter_form = function() {
    let filter_month = $("#sel-filter-month").val();
    let filter_cat = $("#sel-filter-cats").val();
    window.location.href = `?filter-month=${filter_month}&filter-cat=${filter_cat}`
};

panel.recipes.empty_trash = function () {
    $.post("/panel/recipes/change/",
        {
            action: "empty_trash",
            csrfmiddlewaretoken: panel.csrftoken
        },
        function (data, status) {
            if (data["success"]) {
                window.location.href = "/panel/recipes/"
            }
            else {
                alert("message" in data ? data["message"] : "An error has occurred!")
            }
        });
};