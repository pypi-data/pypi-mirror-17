function create_infinite_canvas(height, width) {
  var div = document.createElement('div');
  div.style.height = height+"px";
  div.style.width =  width+"px";
  div.id = "viewer";
  document.body.appendChild(div);

  var viewer = OpenSeadragon({
      id: "viewer",
      tileSources: 'images/0.dzi',
      autoResize: false,
      showNavigationControl: false,
      mouseNavEnabled: false,
      preserveViewport: true,
      immediateRender: false,
      visibilityRatio:1.0
  });

  function fade(old_image, new_image) {
  
  }
   

  var lastImage;
  viewer.addHandler('open', function openHandler() {
    lastImage = viewer.world.getItemAt(0);
  });

  div.style.display = 'none';
  viewer.z = 0
  viewer.setZ = function(delta_z) {
    //TODO check for max or min z
    viewer.z += delta_z;
    viewer.addTiledImage({
      tileSource: "images/" + viewer.z + ".dzi",
      x: 0,
      y: 0,
      opacity:0.01,
      success: function(event) {
        var image = event.item;
        image.addOnceHandler('fully-loaded-change', function() {
          var scalar = {t:0.0};
          new TWEEN.Tween(scalar).to({t: 1.0}, 1)
          .onUpdate(function () {
              image.opacity = scalar.t;
              image._needsDraw = true;
              lastImage.opacity = 1.0 - scalar.t;
              lastImage._needsDraw = true;
          }).onComplete(function () {
              viewer.world.removeItem(lastImage);
              lastImage = image;
          }).start();
              });
      }
    });
  
  };

  //Create channel canvas
  var channel = document.createElement('canvas');
  channel.width = viewer.drawer.canvas.width;
  channel.height = viewer.drawer.canvas.height;
  viewer.channel = channel;
  var ctx = channel.getContext('2d');

  viewer.update =  function() {
    var imageData = viewer.drawer.context.getImageData(0,0,channel.width, channel.height);
    var data = imageData.data;

    //Display channel
    // for (var i = 0; i < data.length; i += 4) {
    //     data[i]       = data[i+3];  // red
    //     data[i+1]     = data[i+3];  // green
    //     data[i+2]     = data[i+3];  // blue
    //     data[i+3]     = 255;
    // }
    //Display segmentation
    // for (var i = 0; i < data.length; i += 4) {
    //     data[i]       = data[i];  // red
    //     data[i+1]     = data[i+1];  // green
    //     data[i+2]     = data[i+2];  // blue
    //     data[i+3]     = 255;
    // }
    //Display both
    // var p = 0.8;
    // for (var i = 0; i < data.length; i += 4) {
    //     data[i]       = data[i+3] * p + data[i] * (1-p);  // red
    //     data[i+1]     = data[i+3] * p + data[i+1] * (1-p);  // green
    //     data[i+2]     = data[i+3] * p + data[i+2] * (1-p);  // blue
    //     data[i+3]     = 255;
    // }
    ctx.putImageData(imageData, 0, 0);
  }

  return viewer;
}