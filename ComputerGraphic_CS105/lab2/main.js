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

const scene = new THREE.Scene()

// plane
let plane = Plane(10, 10, 0xf0a000)

plane.rotation.x = Math.PI / 2
plane.rotation.z = Math.PI / 4
plane.position.y -= 1
plane.position.z -= 2
scene.add(plane)

// box
let box = Box(3, 4, 5, 0xf0a0aa)
box.rotation.y -= 2
box.rotation.z -= 2
box.position.z -= 3
box.position.y += 3

scene.add(box)

// cone
let cone = Cone(1, 2, 3, 0xf0e0aa)
cone.rotation.z = Math.PI / 4
scene.add(cone)

// cylinder
let cylinder = Cylinder(1, 1, 1, 10, 0x1910110)
cylinder.rotation.z -= Math.PI / 4
cylinder.position.x -= 3
cylinder.position.y += 1
scene.add(cylinder)

const camera = new THREE.PerspectiveCamera(
    75,
    window.innerWidth / window.innerHeight,
    1,
    1000
)

camera.position.x = 1
camera.position.y = 2
camera.position.z = 5
camera.lookAt(new THREE.Vector3(0, 0, 0))

const renderer = new THREE.WebGLRenderer()

renderer.setSize(window.innerWidth, window.innerHeight)

document.body.appendChild(renderer.domElement)

renderer.render(scene, camera)