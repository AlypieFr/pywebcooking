pywebcooking = {};

pywebcooking.init = function (page, ...args) {
    if (page === "panel") {
        pywebcooking.panel.init(...args);
    }
    else if (page === "panel-recipes") {
        pywebcooking.panel.recipes.init(...args);
    }
    else if (page === "panel-recipe") {
        pywebcooking.panel.recipe.init(...args);
    }
};