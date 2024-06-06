import * as THREE from 'three'
import * as dat from 'dat'
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';


function Plane(h, w, material) {
    let geometry = new THREE.PlaneGeometry(h, w);
    material.side = THREE.DoubleSide

    let mesh = new THREE.Mesh(
        geometry,
        material
    )
    mesh.receiveShadow=true
    return mesh
}

function Box(w, h, d, material) {
    let geometry = new THREE.BoxGeometry(w, h, d);
    let mesh = new THREE.Mesh(
        geometry,
        material
    )
    mesh.castShadow = true
    return mesh
}

function Sphere(r, material) {
    let geometry = new THREE.SphereGeometry(r, 24, 24);

    let mesh = new THREE.Mesh(
        geometry,
        material
    )
    mesh.castShadow=true
    return mesh
}

function Cone(r, h, rs, material) {
    let geometry = new THREE.ConeGeometry(r, h, rs)
    let mesh = new THREE.Mesh(geometry, material);
    mesh.castShadow = true
    return mesh
}

function Cylinder(rt, rb, h, rs, material) {
    let geometry = new THREE.CylinderGeometry(rt, rb, h, rs);
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

function getBoxGrid(amount, separationMultiplier, material) {
    var group = new THREE.Group();

    for (var i = 0; i < amount; i++) {
        var obj = Box(1, 1, 1, material);
        obj.position.x = i * separationMultiplier;
        obj.position.y = obj.geometry.parameters.height / 2;
        group.add(obj);
        for (var j = 1; j < amount; j++) {
            var obj = Box(1, 1, 1, material);
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

function getMaterial(type, color) {
    var selectedMaterial;
    var materialColor = { color: color === undefined ? "rgb(255, 255, 255)" : color };
    switch (type) {
        case "basic":
            selectedMaterial = new THREE.MeshBasicMaterial(materialColor);
            break;
        case "lambert":
            selectedMaterial = new THREE.MeshLambertMaterial(materialColor);
            break;
        case "phong":
            selectedMaterial = new THREE.MeshPhongMaterial(materialColor);
            break;
        case "standard":
            selectedMaterial = new THREE.MeshStandardMaterial(materialColor);
            break;
        default:
            selectedMaterial = new THREE.MeshBasicMaterial(materialColor);
            break;
    }
    return selectedMaterial;
}

function init(){

    const scene = new THREE.Scene()
    var gui = new dat.GUI()
    // scene.fog = new THREE.FogExp2(0xffffff, 0.05);

    
    
    let clock = new THREE.Clock()
    
    
    let plane_material = getMaterial("phong", "rgb(255, 255, 255)");
    let plane = Plane(30, 30, plane_material)
    
    let sphere_material = getMaterial("phong", "rgb(255, 255, 255)");
    let sphere =  Sphere(2, sphere_material)

    sphere_material.shininess = 100
    
    let light_left = get_spot_light(50)
    let light_right = get_spot_light(50)

    
    sphere.position.y = sphere.geometry.parameters.radius
    plane.rotation.x = Math.PI /2

    
    light_left.position.set(-5, 2, -4)
    light_right.position.set(5, 2, -4)
    
    var loader = new THREE.TextureLoader();
    plane_material.map = loader.load("https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Concrete_texture.jpg/800px-Concrete_texture.jpg?20100503020719");
    plane_material.bumpMap = loader.load("https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Concrete_texture.jpg/800px-Concrete_texture.jpg?20100503020719");
    plane_material.Scale = 0.01;


    var maps = ["map", "bumpMap"];
    maps.forEach((mapName) => {
        var textures = plane_material[mapName];
        textures.wrapS = THREE.RepeatWrapping;
        textures.wrapT = THREE.RepeatWrapping;
        textures.repeat.set(1.5, 1.5);
    });

    scene.add(plane);
    scene.add(sphere);
    scene.add(light_left);
    scene.add(light_right);


    var folder1 = gui.addFolder("Light Left");
    folder1.add(light_left, "intensity", 0, 100);
    folder1.add(light_left.position, "x", -5, 15);
    folder1.add(light_left.position, "y", -5, 15);
    folder1.add(light_left.position, "z", -5, 15);

    var folder2 = gui.addFolder("Light Right");
    folder2.add(light_right, "intensity", 0, 100);
    folder2.add(light_right.position, "x", -5, 15);
    folder2.add(light_right.position, "y", -5, 15);
    folder2.add(light_right.position, "z", -5, 15);
    
    
    
    var folder3 = gui.addFolder("Materials");
    folder3.add(sphere_material, "shininess", 0, 1000);
    
    
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
    
    camera.position.x = 3
    camera.position.y = 4
    camera.position.z = 10


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

    controls.update()

    requestAnimationFrame(function(){
        update(renderer, scene, camera, controls, clock)
    })

}

var scene = init()