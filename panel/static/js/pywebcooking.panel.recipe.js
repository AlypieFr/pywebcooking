if (!pywebcooking || !pywebcooking.panel) {
    throw "panel was not included!"
}

pywebcooking.panel.recipe = {};

pywebcooking.panel.recipe.init = function (lang) {
    pywebcooking.panel.recipe.init_events(lang);
};

pywebcooking.panel.recipe.init_events = function (lang) {
    // Datetime picker:
    $(".datepicker").datetimepicker({
        format: "DD/MM/YYYY HH:mm",
        locale: lang
    });
    let placeholder = 'dd/mm/yyyy hh:mm';
    if (lang.split("-")[0] === "fr")
        placeholder = 'jj/mm/aaaa hh:mm';
    $('.datemask').inputmask("datetime", {
        mask: "1/2/y h:s",
        placeholder: placeholder,
        alias: "dd/mm/yyyy"
    });

    // Save & quit:
    $("form#recipe-form input[type=button]#save-and-quit").click(function() {
        pywebcooking.panel.recipe.save(true);
    });

    // Save:
    $("form#recipe-form input[type=button]#save").click(function() {
        pywebcooking.panel.recipe.save(false);
    });

    // Cancel:
    $("form#recipe-form input[type=button]#cancel").click(pywebcooking.panel.recipe.exit);
};

pywebcooking.panel.recipe.exit = function () {
    window.location.href = "/panel/" + django.gettext("recipes");
};

pywebcooking.panel.recipe.save = function(exit=true) {
    if ($("#recipe-form").validate()) {
        $.ajax({
            url: window.location.href,
            type: "post",
            data: $("#recipe-form").serialize(),
            success: function (data) {
                console.log(data);
            }
        });
    }
};