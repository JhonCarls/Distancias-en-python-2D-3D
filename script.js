let scene, camera, renderer, controls;
let points = [];
let lines = [];

init();
animate();

function init() {
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0xeeeeee);

    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(10, 10, 10);

    renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.getElementById('container').appendChild(renderer.domElement);

    const gridHelper = new THREE.GridHelper(20, 20);
    scene.add(gridHelper);

   const axesHelper = new THREE.AxesHelper(10);
    scene.add(axesHelper);

    const geometry = new THREE.BoxGeometry(10, 10, 10);
    const edges = new THREE.EdgesGeometry(geometry);
    const lineMaterial = new THREE.LineBasicMaterial({ color: 0xFFFFFF });
    const cube = new THREE.LineSegments(edges, lineMaterial);
    scene.add(cube);

    window.addEventListener('resize', onWindowResize, false);

    document.getElementById('addPointsButton').addEventListener('click', addPoints);

    controls = new THREE.OrbitControls(camera, renderer.domElement);
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
}

function addPoints() {
    const input = prompt("Ingrese las coordenadas de los puntos (formato x1,y1,z1 x2,y2,z2):");
    if (input) {
        try {
            const newPoints = input.split(' ').map(p => {
                const [x, y, z] = p.split(',').map(Number);
                if (isNaN(x) || isNaN(y) || isNaN(z)) {
                    throw new Error("Formato inválido");
                }
                return new THREE.Vector3(x, y, z);
            });

            newPoints.forEach(point => {
                points.push(point);
                addPointToScene(point);
            });

            if (points.length >= 2) {
                const p1 = points[points.length - 2];
                const p2 = points[points.length - 1];
                addLineToScene(p1, p2);
            }
        } catch (error) {
            alert("Formato inválido. Ingrese las coordenadas como x1,y1,z1 x2,y2,z2");
        }
    }
}

function addPointToScene(point) {
    const geometry = new THREE.SphereGeometry(0.1, 32, 32);
    const material = new THREE.MeshBasicMaterial({ color: 0x0000ff });
    const sphere = new THREE.Mesh(geometry, material);
    sphere.position.copy(point);
    scene.add(sphere);

    const label = createLabel(`(${point.x},${point.y},${point.z})`);
    label.position.copy(point).add(new THREE.Vector3(0.3, 0.3, 0));
    scene.add(label);
}

function addLineToScene(p1, p2) {
    const material = new THREE.LineBasicMaterial({ color: 0xff0000 });
    const geometry = new THREE.BufferGeometry().setFromPoints([p1, p2]);
    const line = new THREE.Line(geometry, material);
    scene.add(line);

    const distance = p1.distanceTo(p2);
    const midPoint = p1.clone().add(p2).divideScalar(2);
    const label = createLabel(distance.toFixed(2));
    label.position.copy(midPoint).add(new THREE.Vector3(0.3, 0.3, 0));
    scene.add(label);
}

function createLabel(text) {
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    context.font = '24px Arial';
    context.fillStyle = 'black';
    context.fillText(text, 0, 24);
    
    const texture = new THREE.CanvasTexture(canvas);
    const spriteMaterial = new THREE.SpriteMaterial({ map: texture });
    const sprite = new THREE.Sprite(spriteMaterial);
    
    return sprite;
}
