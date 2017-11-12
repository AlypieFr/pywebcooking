panel = {};

panel.init = function(csrftoken) {
    panel.csrftoken = csrftoken;
};

panel.notify = function(message, delay=5000, type="info", url=null) {
    $.notify({
            message: message,
            url: url,
            target: "notify-target"
        },{
            type: type,
            placement: {
                from: "top",
                align: "center"
            },
            delay: delay,
            animate: {
                enter: 'animated fadeInDown',
                exit: 'animated fadeOutUp'
            },
        })
};