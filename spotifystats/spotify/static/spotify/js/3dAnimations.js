var scene = new THREE.Scene();

// Load Camera Perspektive
var camera = new THREE.PerspectiveCamera(
	25,
	window.innerWidth / window.innerHeight,
	1,
	20000
);
camera.position.set(1, 1, 20);
// Load a Renderer
var renderer = new THREE.WebGLRenderer({ alpha: true });
renderer.setPixelRatio(window.devicePixelRatio);
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Load Light
var ambientLight = new THREE.AmbientLight(0xcccccc);
scene.add(ambientLight);

var directionalLight = new THREE.DirectionalLight(0xffffff);
directionalLight.position.set(0, 1, 1).normalize();
scene.add(directionalLight);

// glTf 2.0 Loader
var loader = new THREE.GLTFLoader();
loader.load('/static/spotify/obj/scene.gltf', function (gltf) {
	var object = gltf.scene;
	gltf.scene.scale.set(2, 2, 2);
	gltf.scene.position.x = 10;
	gltf.scene.position.y = 8;
	gltf.scene.position.z = 10;
});

function animate() {
	render();
	requestAnimationFrame(animate);
}

function render() {
	renderer.render(scene, camera);
}

render();
animate();
