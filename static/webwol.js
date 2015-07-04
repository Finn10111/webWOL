$(document).ready(function() {
    pingHosts();
    function pingHosts() {
        setTimeout(pingHosts,5000);
        $(".ping").each(function(index, element) {
            var ip = $(this).attr('id');
            $.ajax({
                method: "POST",
                url: "/ping/"+ip,
            })
            .done(function( data ) {
                if ( data == "1" )
                {
                    var msg = "offline";
                    var css = "label-danger";
                }
                else if ( data == "0" )
                {
                    var msg = "online";
                    var css = "label-success";
                }
                else
                {
                    var msg = "unknown";
                    var css = "label-default";
                }
                $(element).html(msg)
                $(element).removeClass('label-danger label-success label-default').addClass(css);
            });
        });
    }
});
