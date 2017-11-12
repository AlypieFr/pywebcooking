if (!panel) {
    throw "panel was not included!"
}

panel.recipe = {};

panel.recipe.init = function (lang) {
    panel.recipe.init_events(lang);
};

panel.recipe.init_events = function (lang) {
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
};