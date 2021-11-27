

$(document).ready(function(){
    "use strict";
    // Initializes the carousel
    $(".start-slide").click(function(){
        $("#myCarousel").carousel('cycle');
    });
    // Stops the carousel
    $(".pause-slide").click(function(){
        $("#myCarousel").carousel('pause');
    });
    // Cycles to the previous item
    $(".prev-slide").click(function(){
        $("#myCarousel").carousel('prev');
    });
    // Cycles to the next item
    $(".next-slide").click(function(){
        $("#myCarousel").carousel('next');
    });
    // Cycles the carousel to a particular frame
    $(".slide-one").click(function(){
        $("#myCarousel").carousel(0);
    });
    $(".slide-two").click(function(){
        $("#myCarousel").carousel(1);
    });
    $(".slide-three").click(function(){
        $("#myCarousel").carousel(2);
    });
});


    // $('.carousel-item:first-child').addClass("active");
    $('.carousel-item img:nth-of-type(1)').addClass("index_item_img");
