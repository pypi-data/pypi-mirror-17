var camera, scene, renderer, geometry, texture, mesh;

var channelTex;
function createPlaneMaterial() {
  //It returns a material for each side of the "plane" which is actually a box
  //where z << x && z << y

  channelTex = new THREE.Texture(viewer.channel, //image
                                      undefined, //mapping
                                      undefined, //wrapS
                                      undefined, //wrapT
                                      THREE.NearestFilter, //magFilter
                                      THREE.NearestFilter  //minFilter
                                      );
  channelTex.flipY = true;
  channelTex.generateMipmaps = false;

  var imageMat = new THREE.MeshBasicMaterial({
    map: channelTex,
    color: 0xFFFFFF,
    opacity: 0.8,
    transparent: true,
  });

  // this seems to disable flickering
  imageMat.polygonOffset = true;
  // positive value is pushing the material away from the screen
  imageMat.polygonOffsetFactor = 0.1; // https://www.opengl.org/archives/resources/faq/technical/polygonoffset.htm

  var plainMat = new THREE.MeshBasicMaterial({
    color: 0xCCCCCC,
    opacity: 0.8,
    transparent: true
  });

  var materials = [
    plainMat,
    plainMat,
    plainMat,
    plainMat,
    imageMat,
    imageMat,
  ];
  return materials;
}

function create_plane() {
  //Plane geometry is the one that holds the electron microscopy image, it has some tickness that's why
  //we are using a box
  var planeGeometry = new THREE.BoxGeometry(1, 1, 0.01);
  planeGeometry.faceVertexUvs[0][10] = [new THREE.Vector2(1, 1), new THREE.Vector2(1, 0), new THREE.Vector2(0, 1)];
  planeGeometry.faceVertexUvs[0][11] = [new THREE.Vector2(1, 0), new THREE.Vector2(0, 0), new THREE.Vector2(0, 1)];
  
  var materials = createPlaneMaterial();
  var plane = new THREE.Mesh(planeGeometry, new THREE.MeshFaceMaterial(materials));
  return plane
};

var camera;
function create_camera(perspFov, orthoFov, viewHeight) {
    function simpleViewHeight(fov, realHeight) {
        function deg2Rad(deg) { return deg / 180 * Math.PI; }
        var radius = realHeight / Math.sin(deg2Rad(fov)) * Math.sin(deg2Rad((180 - fov) / 2));
        return fov * radius;
    }

    var realCamera = new THREE.PerspectiveCamera(
        perspFov, // Field of View (degrees)
        window.innerWidth / window.innerHeight, // Aspect ratio (set later) TODO why?
        0.2, // Inner clipping plane // TODO, at 0.1 you start to see white artifacts when scrolling quickly
        1300 // Far clipping plane
    );

    realCamera.position.set(0, 0, simpleViewHeight(perspFov, viewHeight) / perspFov);
    realCamera.up.set(0, 1, 0);
    realCamera.lookAt(new THREE.Vector3(0, 0, 0));

    return {
        realCamera: realCamera,
        perspFov: perspFov,
        orthoFov: orthoFov,
        _viewHeight: viewHeight,
        fakeViewHeight:simpleViewHeight(perspFov, viewHeight),
        set viewHeight(vH) {
          this._viewHeight = vH;
          this.fakeViewHeight = simpleViewHeight(perspFov, vH);
          this.fov = this.fov;  //it is calling get on and then set
        },
        get viewHeight() {
          return this._viewHeight;
        },
        get fov() {
          return realCamera.fov;
        },
        set fov(fov) {
          realCamera.fov = fov; 
          realCamera.position.z =  this.fakeViewHeight / fov;
          realCamera.updateProjectionMatrix();
        }
    };
}

var plane;
var pivot;
function init() {
    
    renderer = new THREE.WebGLRenderer({
        antialias: true,
        preserveDrawingBuffer: true, // TODO, why?
        alpha: true,
    });
    renderer.setSize(width, height);
    mydiv.appendChild(renderer.domElement);
    
    scene = new THREE.Scene();
  
    camera = create_camera(40, 10.0, 0.75);
    // camera.fov = camera.orthoFov;
    scene.add(camera.realCamera);

    pivot = new THREE.Object3D();
    scene.add(pivot);

    plane = create_plane();
    pivot.add(plane);
}