var canvas = document.querySelector("#jiong");
var ctx = canvas.getContext('2d');

function create_image(pixels) {
    // pixels are (x, y, r, g, b)
    var width = options['width'], height = options['height'];
    var zoom = options['zoom'];
    var imagedata = ctx.createImageData(width * zoom, height * zoom);
    pixels.forEach(function(pixel) {
        var y = pixel[1] * zoom;
        for (var i = 0; i < zoom; i++) {
            var row = width * zoom * y;
            var x = pixel[0] * zoom;
            for (var j = 0; j < zoom; j++) {
                imagedata.data[(row+ x) * 4] = pixel[2];
                imagedata.data[(row + x) * 4 + 1] = pixel[3];
                imagedata.data[(row + x) * 4 + 2] = pixel[4];
                imagedata.data[(row + x) * 4 + 3] = 255;
                x++;
            }
            y++;
        }
    });
    return imagedata;
}

function draw(pixels) {
    ctx.putImageData(create_image(pixels), 0, 0);
}

function to_color(color) {
    return 'rgb(' + color[0] + ',' + color[1] + ',' + color[2] + ')';
}

function getData() {
    var request = new XMLHttpRequest();
    request.open('GET', '/i', true);
    request.onload = function() {
        var response = JSON.parse(request.responseText);
        options = response['options'];
        images = response['images'];
        canvas.width = options['width'] * options['zoom'];
        canvas.height = options['height'] * options['zoom'];
        canvas.style.backgroundColor = to_color(options['background']);
        if (images.length == 1) {
            draw(images[0], options['width'], options['height'])
        } else if (images.length > 1) {
            animate();
        }
    }
    request.send();
}

function animate() {
    if (!options['loop'] && frame / options['slow'] >= images.length) {
        return ;
    }
    window.requestAnimationFrame(animate);
    if (frame % options['slow'] == 0) {
        draw(images[(frame / options['slow']) % images.length]);
    }
   frame++;
 }

var frame = 0, options = {}, images = [];
getData();
