import * as THREE from 'three'
import * as dat from 'dat'
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';


function Plane(h, w, color) {
    let geometry = new THREE.PlaneGeometry(h, w);
    let material = new THREE.MeshPhongMaterial(
        {
            color: color,
            side: THREE.DoubleSide
        }
    )
    let mesh = new THREE.Mesh(
        geometry,
        material
    )
    mesh.receiveShadow=true
    return mesh
}

function Box(w, h, d, color) {
    let geometry = new THREE.BoxGeometry(w, h, d);
    let material = new THREE.MeshPhongMaterial(
        { color: color }
    );
    let mesh = new THREE.Mesh(
        geometry,
        material
    )
    mesh.castShadow = true
    return mesh
}

function Sphere(r, color) {
    let geometry = new THREE.SphereGeometry(r, 24, 24);
    let material = new THREE.MeshBasicMaterial(
        { color: color }
    );
    let mesh = new THREE.Mesh(
        geometry,
        material
    )
    return mesh
}

function Cone(r, h, rs, color) {
    let geometry = new THREE.ConeGeometry(r, h, rs);
    let material = new THREE.MeshPhongMaterial({ color: color });
    let mesh = new THREE.Mesh(geometry, material);
    mesh.castShadow = true
    return mesh
}

function Cylinder(rt, rb, h, rs, color) {
    let geometry = new THREE.CylinderGeometry(rt, rb, h, rs);
    let material = new THREE.MeshPhongMaterial({ color: color });
    let mesh = new THREE.Mesh(geometry, material);
    mesh.castShadow = true
    return mesh
}

function get_point_light(intensity){
    let light = new THREE.PointLight(0xffffff, intensity)
    light.castShadow = true
    return light
}

function get_ambient_light(intensity){
    let light = new THREE.AmbientLight(0x102050, intensity)
    return light
}



function get_spot_light(intensity){
    let light = new THREE.SpotLight(0xffffff, intensity)
    light.castShadow = true
    light.shadow.bias=0.001
    light.shadow.mapSize.width=2048
    light.shadow.mapSize.height=2048
    return light
}

function get_directional_light(intensity){
    let light = new THREE.DirectionalLight(0xffffff, intensity)
    light.castShadow = true
    light.shadow.bias=0.001
    light.shadow.mapSize.width=2048
    light.shadow.mapSize.height=2048

    light.shadow.camera.left = -10
    light.shadow.camera.right = 10
    light.shadow.camera.top = 10
    light.shadow.camera.bottom = -10
    return light
}

function getBoxGrid(amount, separationMultiplier, color) {
    var group = new THREE.Group();

    for (var i = 0; i < amount; i++) {
        var obj = Box(1, 1, 1, color);
        obj.position.x = i * separationMultiplier;
        obj.position.y = obj.geometry.parameters.height / 2;
        group.add(obj);
        for (var j = 1; j < amount; j++) {
            var obj = Box(1, 1, 1, color);
            obj.position.x = i * separationMultiplier;
            obj.position.y = obj.geometry.parameters.height / 2;
            obj.position.z = j * separationMultiplier;
            group.add(obj);
        }
    }
    group.position.x = -((separationMultiplier * (amount - 1)) / 2);
    group.position.z = -((separationMultiplier * (amount - 1)) / 2);

    return group;
}

function init(){

    const scene = new THREE.Scene()
    // scene.fog = new THREE.FogExp2(0xffffff, 0.05);

    var gui = new dat.GUI()

    let clock = new THREE.Clock()
    
    
    let light = get_directional_light(11)
    let p_sphere = Sphere(0.3, 0xffffff)

    let ambient_light = get_ambient_light(1)
    
    let helper = new THREE.CameraHelper(light.shadow.camera)
    light.add(p_sphere)

    // light.position.x = 10
    light.position.z = -10
    light.intensity=5

    gui.add(light, "intensity", 0, 50)
    // gui.add(light, "penumbra", 0, 1)

    gui.add(light.position, "y", -10, 10)
    gui.add(light.position, "x", -10, 10)
    gui.add(light.position, "z", -40, 0)

    // plane
    let plane = Plane(50, 50, 0xf0a000)

    plane.add(light)

    plane.name = "pl1"
    plane.rotation.x = Math.PI / 2
    plane.rotation.z = Math.PI / 4
    // plane.position.y -= 1
    // plane.position.z -= 2
    scene.add(plane)
    scene.add(ambient_light)

    scene.add(helper)

    // box
    let box_grid = getBoxGrid(10, 2.5, 0xf0a000)

    box_grid.name = "box_grid"

    // box_grid.rotation.x = Math.PI / 2
    box_grid.position.y=0.1
    scene.add(box_grid)
    
    // cone
    let cone = Cone(1, 2, 3, 0xf0e0aa)
    cone.rotation.z = Math.PI / 4
    cone.position.z -= 4
    cone.position.x += 5
    cone.position.y += 5
    cone.name = "cone1"
    
    plane.add(cone)
    
    // cylinder
    let cylinder = Cylinder(1, 1, 1, 10, 0x1910110)
    cylinder.rotation.z -= Math.PI / 4
    cylinder.position.x -= 3
    cylinder.position.y += 1
    cylinder.position.z -= 5
    plane.add(cylinder)
    
    const camera = new THREE.PerspectiveCamera(
        75,
        window.innerWidth / window.innerHeight,
        1,
        1000
    )

    // let camera = new THREE.OrthographicCamera(
    //     -15,
    //     15,
    //     15,
    //     -15,
    //     1,
    //     1000
    // )
    
    // camera.position.x = 3
    // camera.position.y = 4
    // camera.position.z = 10
    let cameraZposition = new THREE.Group()
    let cameraYposition = new THREE.Group()

    let cameraYrotation = new THREE.Group()
    let cameraXrotation = new THREE.Group()
    let cameraZrotation = new THREE.Group()

    cameraZposition.add(camera)
    cameraYposition.add(cameraZposition)
    cameraXrotation.add(cameraYposition)
    cameraYrotation.add(cameraXrotation)
    cameraZrotation.add(cameraYrotation)

    cameraZposition.name = "cameraZposition"
    cameraYrotation.name = "cameraYrotation"
    cameraXrotation.name = "cameraXrotation"
    cameraYposition.name = "cameraYposition"

    cameraZposition.position.z=100
    cameraYposition.position.y=2

    gui.add(cameraZposition.position, 'z', 0, 100)
    gui.add(cameraYrotation.rotation, 'y', -Math.PI, Math.PI)
    gui.add(cameraXrotation.rotation, 'x', -Math.PI, Math.PI)
    gui.add(cameraZrotation.rotation, 'z', -Math.PI, Math.PI)

    scene.add(cameraZrotation)

    camera.lookAt(new THREE.Vector3(0, 0, 0))
    
    const renderer = new THREE.WebGLRenderer()

    renderer.shadowMap.enabled = true

    renderer.setClearColor(0x202020)
    
    renderer.setSize(window.innerWidth, window.innerHeight)
    
    document.body.appendChild(renderer.domElement)
    
    let controls = new OrbitControls(camera, renderer.domElement)
    
    update(renderer, scene, camera, controls, clock)
    
    return scene
}

function update(renderer, scene, camera, controls, clock){
    renderer.render(scene, camera)

    let timeElapsed = clock.getElapsedTime()

    let cameraZposition = scene.getObjectByName("cameraZposition")
    let cameraYrotation = scene.getObjectByName("cameraYrotation")
    let cameraZrotation = scene.getObjectByName("cameraZrotation")
    let cameraXrotation = scene.getObjectByName("cameraXrotation")
    let cameraYposition = scene.getObjectByName("cameraYposition")

    cameraZposition.position.z -= 0.25

    let plane = scene.getObjectByName("pl1")
    
    // plane.rotation.x += 0.001
    // plane.rotation.z += 0.001
    let box_grid = scene.getObjectByName("box_grid")
    box_grid.children.forEach((child, index) => {
        child.scale.y = (Math.sin(timeElapsed * 5 + index) + 1)/10 + 0.001
        child.position.y = child.scale.y/2
    });


    let cone = scene.getObjectByName("cone1")

    cone.rotation.z += 0.01
    cone.rotation.x += 0.01
    cone.scale.x += 0.01


    // camera.position.z += 0.005
    // camera.rotation.z += 0.002

    controls.update()

    requestAnimationFrame(function(){
        update(renderer, scene, camera, controls, clock)
    })

}

var scene = init()