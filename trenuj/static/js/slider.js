        $('.link').click(function(){
            var ind=3;
            ind--;
            $('#slides').superslides('animate' , ind)
         });
/*
        document.onclick = function() {
            if($('#register').css('display') == 'block')
            {
                $('.slides-navigation').css("display","none");
            }
            else
            {
                $('.slides-navigation').css("display","block");
            }
        };

        $(document).on('keyup', function() {
                if($('#register').css('display') == 'block')
                {
                    $('.slides-navigation').css("display","none");
                }
                else
                {
                    $('.slides-navigation').css("display","block");
                }
        });

        setInterval(function() {
                if($('#register').css('display') == 'block')
                {
                    $('.slides-navigation').css("display","none");
                }
                else
                {
                    $('.slides-navigation').css("display","block");
                }
        },0.1);
*/