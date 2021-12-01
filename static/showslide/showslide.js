$(document).ready(() => {
    // Initializes the carousel
    $('.start-slide').click(() => {
        $('#myCarousel').carousel('cycle');
    });
    // Stops the carousel
    $('.pause-slide').click(() => {
        $('#myCarousel').carousel('pause');
    });
    // Cycles to the previous item
    $('.prev-slide').click(() => {
        $('#myCarousel').carousel('prev');
    });
    // Cycles to the next item
    $('.next-slide').click(() => {
        $('#myCarousel').carousel('next');
    });
    // Cycles the carousel to a particular frame
    $('.slide-one').click(() => {
        $('#myCarousel').carousel(0);
    });
    $('.slide-two').click(() => {
        $('#myCarousel').carousel(1);
    });
    $('.slide-three').click(() => {
        $('#myCarousel').carousel(2);
    });
});

    // $('.carousel-item:first-child').addClass("active");
    $('.carousel-item img:nth-of-type(1)').addClass('index_item_img');
