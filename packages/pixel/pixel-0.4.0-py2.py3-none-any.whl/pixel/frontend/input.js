function MouseRotationHandler(element) {
    function animateToQuaternion(target, duration, callback) {
        var start = new THREE.Quaternion().copy(pivot.quaternion);
        scalar = {t:0}
        new TWEEN.Tween(scalar).to({t: 1}, duration).onUpdate(
            function () {
                THREE.Quaternion.slerp(start, target, pivot.quaternion, scalar.t);
                // camera.fov = Math.min(camera.fov, camera.orthoFov * scalar.t + camera.perspFov * (1-scalar.t));
            })
        .onComplete(
            function () {
                pivot.quaternion.copy(target);
                pivot.setRotationFromQuaternion(target);
                callback();
        }).start();
    }


    function rotationDown(e) {
        start.copy( getMouseProjectionOnBall(event.pageX, event.pageY));
        end.copy(start);
        if (e.ctrlKey) { //Rotate the plane
          watchRotation();    
        }
    }

    function rotationMove(e) {
        end.copy( getMouseProjectionOnBall(event.pageX, event.pageY));
        var angle = Math.acos( start.dot( end ) / start.length() / end.length() );
        if (!angle ) { return; }
        axis.crossVectors( start, end ).normalize();
        angle *= 1.0 //rotateSpeed
        quaternion.setFromAxisAngle( axis, angle ).normalize();
        var currQuaternion = pivot.quaternion;
        currQuaternion.multiplyQuaternions( quaternion, currQuaternion).normalize();
        pivot.setRotationFromQuaternion(currQuaternion);
        start.applyQuaternion( quaternion );
    }

    function rotationUp(e) {
        stopRotation();
        var target =  new THREE.Quaternion(0,0,0,1);
        animateToQuaternion(target, 250, function(){
            console.log('done rotating');
        });
    }

    function stopRotation() {
        element.removeEventListener("mousemove", rotationMove);
        element.removeEventListener("mouseup", rotationUp);
    }

    function watchRotation() {
        element.addEventListener("mousemove", rotationMove, false);
        element.addEventListener("mouseup", rotationUp, false)
    }
    element.addEventListener("mousedown", rotationDown , false);

    var start = new THREE.Vector3();
    var end = new THREE.Vector3();
    var axis = new THREE.Vector3();
    var quaternion = new THREE.Quaternion();

 }

function MouseDragHandler(element) {
    function dragDown(e) {
        if (!e.ctrlKey) { //Rotate the plane
          watchRotation();    
        }
        lastpos = {x:e.x, y:e.y}
    }
    function dragMove(e) {
        zoom_scale = 1.0 / viewer.viewport._oldZoom * 0.003
        new_pos = {x:e.x, y:e.y}
        delta = {x: (lastpos.x-new_pos.x)*zoom_scale, 
                 y: (lastpos.y-new_pos.y)*zoom_scale};
        viewer.viewport.panBy(delta)
        lastpos = new_pos
    }
    function dragUp(e) {
        stopDrag();
    }
    function stopDrag() {
        element.removeEventListener("mousemove", dragMove);
        element.removeEventListener("mouseup", dragUp);
    }
    function watchRotation() {
        element.addEventListener("mousemove", dragMove, false);
        element.addEventListener("mouseup", dragUp, false)
    }

    var lastpos;
    element.addEventListener("mousedown", dragDown , false);
}

var mouseOnBall = new THREE.Vector3();
function getMouseProjectionOnBall(pageX, pageY) {
    var minDist = Math.min(width, height);
    var circleRadius = minDist / 2.2;
    mouseOnBall.set(
      ( pageX - width / 2 ) / circleRadius,
      ( height / 2 - pageY ) / circleRadius,
      0.0
    );
    var length = mouseOnBall.length();
    if (length > 1.0) {
      mouseOnBall.normalize();
    } else {
      mouseOnBall.z = Math.sqrt( 1.0 - length * length );
    }
    return mouseOnBall;
}

MouseDragHandler(mydiv);
MouseRotationHandler(mydiv);
function MouseWheelHandler(e) {
    event.preventDefault();
    event.stopPropagation();
    var delta = Math.max(-1, Math.min(1, (e.wheelDelta || -e.detail)));
    if (e.shiftKey) {
        viewer.viewport.zoomBy(1+ .1 * delta)   
    }
    else {
        viewer.setZ(delta);
    }

    return false;
}
mydiv.addEventListener("mousewheel", MouseWheelHandler, false);