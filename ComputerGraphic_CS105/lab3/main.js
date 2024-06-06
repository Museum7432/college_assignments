import * as THREE from 'three'

function Plane(h, w, color) {
    let geometry = new THREE.PlaneGeometry(h, w);
    let material = new THREE.MeshBasicMaterial(
        {
            color: color,
            side: THREE.DoubleSide
        }
    )
    let mesh = new THREE.Mesh(
        geometry,
        material
    )
    return mesh
}

function Box(w, h, d, color) {
    let geometry = new THREE.BoxGeometry(w, h, d);
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
    let material = new THREE.MeshBasicMaterial({ color: color });
    let cone = new THREE.Mesh(geometry, material);
    return cone
}

function Cylinder(rt, rb, h, rs, color) {
    let geometry = new THREE.CylinderGeometry(rt, rb, h, rs);
    let material = new THREE.MeshBasicMaterial({ color: color });
    let cylinder = new THREE.Mesh(geometry, material);
    return cylinder
}

function init(){

    const scene = new THREE.Scene()
    scene.fog = new THREE.FogExp2(0xffffff, 0.05);
    
    // plane
    let plane = Plane(40, 50, 0xf0a000)

    
    plane.name = "pl1"
    plane.rotation.x = Math.PI / 2
    plane.rotation.z = Math.PI / 4
    plane.position.y -= 1
    plane.position.z -= 2
    scene.add(plane)

    // box
    let box = Box(3, 4, 5, 0xf0a0aa)
    box.rotation.y -= 2
    box.position.z -= 4
    box.position.y -= 3

    box.name = "box1"
    
    plane.add(box)
    
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
    
    camera.position.x = 3
    camera.position.y = 4
    camera.position.z = 10
    camera.lookAt(new THREE.Vector3(0, 0, 0))
    
    const renderer = new THREE.WebGLRenderer()

    renderer.setClearColor(0xffffff)
    
    renderer.setSize(window.innerWidth, window.innerHeight)
    
    document.body.appendChild(renderer.domElement)
    
    
    update(renderer, scene, camera)
    
    return scene
}

function update(renderer, scene, camera){
    renderer.render(scene, camera)

    let plane = scene.getObjectByName("pl1")

    // plane.rotation.x += 0.001
    // plane.rotation.z += 0.001

    let box = scene.getObjectByName("box1")

    box.rotation.z += 0.02
    box.rotation.x += 0.02

    let cone = scene.getObjectByName("cone1")

    cone.rotation.z += 0.01
    cone.rotation.x += 0.01
    cone.scale.x += 0.01


    camera.position.z += 0.005
    camera.rotation.z += 0.002

    requestAnimationFrame(function(){
        update(renderer, scene, camera)
    })

}

var scene = init()