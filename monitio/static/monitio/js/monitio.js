if (window.monitio == undefined) window.monitio = {};

monitio = {
    messages: [],
    placeholder: null,
    theme: null,
    themes: {},
    levels: {
        // messages -> django.contrib.messages.constants
        10: "debug",
        20: "info",
        25: "success",
        30: "warning",
        40: "error",

        // persistent messages -> monitio.constants
        110: "debug",
        120: "info",
        125: "success",
        130: "warning",
        140: "error"
    }
};

monitio.themes.jqueryui = {
    getHTML: function (message) {
        // TODO jezeli message nei ma PK, to nie wypisuj linku do zamkniecia go
        var subject = message.subject;
        if (subject)
            subject = subject + ": ";

        return $("<div/>")
            .addClass("ui-widget")
            .append([
                $("<div/>")
                    .addClass("ui-corner-all " + monitio.theme.getCSSClasses(message.level))
                    .css("padding", "0 .7em")
                    .css("margin-top", "5px")
                    .css("overflow", "auto")
                    .append([
                                $("<span/>")
                                    .addClass("ui-icon " + monitio.theme.getCSSIcons(message.level))
                                    .css("float", "left")
                                    .css("margin-right", ".3em"),
                                $("<div/>")
                                    .css("float", "left")
                                    .css("width", "85%")
                                    .append([
                                        $("<strong/>").text(subject),
                                        message.message
                                    ]),
                                $("<div/>")
                                    .css("float", "right")
                                    .append([
                                        $("<a>close</a>")
                                            .addClass("message-close icon")
                                            .attr("href", " /messages/mark_read/" + message.pk + "/")
                                    ])
                    ])
            ]);


    },

    getCloseAllHTML: function () {
        return $("<div/>")
            .addClass("ui-widget message-close-all")
            .append([
                $("<div/>")
                    .addClass("ui-corner-all ui-state-highlight")
                    .css("margin-top", "5px")
                    .css("padding", "0 .8em")
                    .append([
                        $("<span/>")
                            .addClass("ui-icon ui-icon-circle-close")
                            .css("float", "left")
                            .css("margin-right", ".3em")
                            .css("margin-top", ".15em"),

                        $("<a/>")
                            .attr("href", "/messages/mark_read/all/")
                            .addClass("message-close-all")
                            .append("close all messages")
                    ])
            ]);
    },

    getCSSClasses: function (level) {
        switch (monitio.levels[level]) {
            case "debug":
            case "success":
            case "info":
                return "ui-state-highlight";
            case "warning":
            case "error":
                return "ui-state-error";
        }
    },

    getCSSIcons: function (level) {
        switch (monitio.levels[level]) {
            case "debug":
                return "ui-icon-script";
            case "success":
            case "info":
                return "ui-icon-info";
            case "warning":
                return "ui-icon-alert";
            case "error":
                return "ui-icon-circle-close";
        }
        return "ui-icon-info";
    }
};

monitio.theme = monitio.themes.jqueryui;

$.widget("monitio.FlashMessage", {

    _create: function () {
        // TODO tutaj tworzenie komunikatu w jquery
        // LUB foundation, w zlaeżności od parametru 'theme'
        // OPCJE to message_text, message_class, message_url też może być
        var element = monitio.theme.getHTML(this.options.message);
        this.element.append(element);
    },

    _setOption: function (key, value) {

    }
});

$.widget("monitio.MessagesPlaceholder", {
    _create: function () {

        var source = new EventSource(this.options.url);
        var self = this;

        source.addEventListener('message', function (e) {
            self.addMessage($.parseJSON(e.data));
        });

        this.element.append("<div/>");
        monitio.placeholder = this.element.children().last();


        $.ajax({
            dataType: 'json',
            url: "/messages/json/",
            success: function (data, status, obj) {
                data.forEach(function (msg) {
                    self.addMessage(msg);
                });
            },
            error: function(err) {
                console.log(err);
                self.addMessage({
                    'level': 40, // error
                    'subject': "Error",
                    'message': "Server error - unable to load messages<br/>(" + err.status + " " + err.statusText + ")",
                    'pk': null
                })
            }
        });

    },

    addMessage: function (msg) {
        monitio.placeholder.append("<div/>");
        monitio.placeholder.children().last().FlashMessage({'message': msg});
        if (monitio.placeholder.children().length == 2) {
            monitio.placeholder.parent().append(
                monitio.theme.getCloseAllHTML());
        }
        ;
    }

});
