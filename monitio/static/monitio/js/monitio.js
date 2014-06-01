if (window.monitio == undefined) window.monitio = {};

monitio = {
    messages: [],
    widget: null,
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
    options: {
        "theme": "jqueryui",
        "initial": []
    },

    _create: function () {

        if (this.options.theme)
            monitio.theme = eval("monitio.themes." + this.options.theme);

        var source = new EventSource(this.options.url);
        var self = this;

        source.addEventListener('message', function (e) {
            self.addMessage($.parseJSON(e.data));
        });

        this.element.append("<div/>");
        monitio.widget = this.element;
        monitio.placeholder = this.element.children().last();

        this.options.initial.forEach(self.addMessage);
    },

    addMessage: function (msg) {
        monitio.placeholder.append("<div/>").attr("is_persistent", msg.is_persistent);

        monitio.placeholder.children().last().FlashMessage({'message': msg});
        if (monitio.placeholder.children().length == 2) {
            monitio.placeholder.parent().append(
                monitio.theme.getCloseAllHTML());
        };
    },

    closeMessage: function(msgDiv, url){

        var removeDiv = function(){
            msgDiv.remove();
            if (monitio.placeholder.children().length==1)
                monitio.placeholder.parent().children().last().remove();
        }

        if (msgDiv.parent().attr("is_persistent")!="true") {
            removeDiv();
            return
        }

        $.ajax({
            url: url,
            method: "GET",
            success: removeDiv
        });
    },

    closeAllMessages: function(){
        $.ajax({
            url: '/messages/mark_read/all/',
            method: "GET",
            success: function(){
                monitio.placeholder.children().remove();
                monitio.placeholder.parent().children().last().remove();
            }
        });

    }

});
