const productos = [
  { id: 1, nombre: "Completo Italiano", categoria: "Italianos", precio: 2500, desc: "Tomate, palta y mayonesa.", img: "https://images.pexels.com/photos/4113504/pexels-photo-4113504.jpeg?auto=compress&cs=tinysrgb&h=400&w=600" },
  { id: 2, nombre: "Italiano Doble", categoria: "Italianos", precio: 3200, desc: "Dos vienesas, doble palta y doble mayonesa.", img: "https://images.pexels.com/photos/4113503/pexels-photo-4113503.jpeg?auto=compress&cs=tinysrgb&h=400&w=600" },
  { id: 3, nombre: "Completo Dinámico", categoria: "Dinámicos", precio: 2600, desc: "Tomate, palta, chucrut y salsa americana.", img: "https://images.pexels.com/photos/4113500/pexels-photo-4113500.jpeg?auto=compress&cs=tinysrgb&h=400&w=600" },
  { id: 4, nombre: "Dinámico XL", categoria: "Dinámicos", precio: 3400, desc: "Versión grande con doble de aderezos.", img: "https://images.pexels.com/photos/4113499/pexels-photo-4113499.jpeg?auto=compress&cs=tinysrgb&h=400&w=600" },
  { id: 5, nombre: "Hot Dog Americano", categoria: "Americanos", precio: 2800, desc: "Mostaza, ketchup y cebolla picada.", img: "https://images.pexels.com/photos/4113501/pexels-photo-4113501.jpeg?auto=compress&cs=tinysrgb&h=400&w=600" },
  { id: 6, nombre: "Americano Queso", categoria: "Americanos", precio: 3100, desc: "Con salsa de queso cheddar derretido.", img: "https://images.pexels.com/photos/6441795/pexels-photo-6441795.jpeg?auto=compress&cs=tinysrgb&h=400&w=600" },
  { id: 7, nombre: "Combo Doggy's", categoria: "Combos", precio: 4200, desc: "Un hot dog a elección, papas y bebida.", img: "https://images.pexels.com/photos/8287715/pexels-photo-8287715.jpeg?auto=compress&cs=tinysrgb&h=400&w=600" },
  { id: 8, nombre: "Combo Doble", categoria: "Combos", precio: 6900, desc: "Dos hot dogs, papas grandes y dos bebidas.", img: "https://images.pexels.com/photos/4113458/pexels-photo-4113458.jpeg?auto=compress&cs=tinysrgb&h=400&w=600" }
];

let carrito = [];
let categoriaActual = "Todos";

const listaProductos = document.getElementById("listaProductos");
const itemsCarrito = document.getElementById("itemsCarrito");
const totalCarrito = document.getElementById("totalCarrito");
const contadorCarrito = document.getElementById("contadorCarrito");
const mensajeCarrito = document.getElementById("mensajeCarrito");

function formatoCLP(n) {
  return "$" + n.toLocaleString("es-CL");
}

function mostrarMensaje(contenedor, texto, tipo) {
  contenedor.innerHTML = `<div class="alert alert-${tipo} mt-2">${texto}</div>`;
}

function mostrarProductos() {
  const lista = categoriaActual === "Todos"
    ? productos
    : productos.filter(p => p.categoria === categoriaActual);

  listaProductos.innerHTML = "";
  lista.forEach(p => {
    listaProductos.innerHTML += `
      <div class="col-12 col-sm-6 col-lg-4">
        <div class="card h-100 tarjeta">
          <img src="${p.img}" class="card-img-top" alt="${p.nombre}">
          <div class="card-body d-flex flex-column">
            <h5 class="card-title">${p.nombre}</h5>
            <p class="card-text">${p.desc}</p>
            <div class="mt-auto d-flex justify-content-between align-items-center">
              <span class="precio">${formatoCLP(p.precio)}</span>
              <button class="btn btn-warning" onclick="agregarAlCarrito(${p.id})">Agregar</button>
            </div>
          </div>
        </div>
      </div>`;
  });
}

document.querySelectorAll("#filtros button").forEach(btn => {
  btn.addEventListener("click", () => {
    categoriaActual = btn.dataset.cat;
    document.querySelectorAll("#filtros button").forEach(b => {
      b.classList.remove("active", "btn-warning");
      b.classList.add("btn-outline-warning");
    });
    btn.classList.remove("btn-outline-warning");
    btn.classList.add("active", "btn-warning");
    mostrarProductos();
  });
});

function agregarAlCarrito(id) {
  const producto = productos.find(p => p.id === id);
  const existente = carrito.find(i => i.id === id);

  if (existente) {
    existente.cantidad++;
  } else {
    carrito.push({ id: producto.id, nombre: producto.nombre, precio: producto.precio, cantidad: 1 });
  }

  mostrarCarrito();
}

function cambiarCantidad(id, cambio) {
  const item = carrito.find(i => i.id === id);
  item.cantidad += cambio;
  if (item.cantidad <= 0) {
    carrito = carrito.filter(i => i.id !== id);
  }
  mostrarCarrito();
}

function quitarDelCarrito(id) {
  carrito = carrito.filter(i => i.id !== id);
  mostrarCarrito();
}

function mostrarCarrito() {
  itemsCarrito.innerHTML = "";
  let total = 0;
  let cantidad = 0;

  if (carrito.length === 0) {
    itemsCarrito.innerHTML = '<li class="list-group-item">Tu carrito está vacío</li>';
  }

  carrito.forEach(item => {
    total += item.precio * item.cantidad;
    cantidad += item.cantidad;
    itemsCarrito.innerHTML += `
      <li class="list-group-item">
        <div class="d-flex justify-content-between">
          <span>${item.nombre}</span>
          <span>${formatoCLP(item.precio * item.cantidad)}</span>
        </div>
        <div class="mt-2">
          <button class="btn btn-sm btn-outline-dark" onclick="cambiarCantidad(${item.id}, -1)">-</button>
          <span class="mx-2">${item.cantidad}</span>
          <button class="btn btn-sm btn-outline-dark" onclick="cambiarCantidad(${item.id}, 1)">+</button>
          <button class="btn btn-sm btn-danger ms-2" onclick="quitarDelCarrito(${item.id})">Quitar</button>
        </div>
      </li>`;
  });

  totalCarrito.innerText = formatoCLP(total);
  contadorCarrito.innerText = cantidad;
}

function obtenerUsuarios() {
  return JSON.parse(localStorage.getItem("usuarios")) || [];
}

function obtenerSesion() {
  return JSON.parse(localStorage.getItem("sesion"));
}

function actualizarSesion() {
  const sesion = obtenerSesion();
  const saludo = document.getElementById("saludo");
  const btnAcceder = document.getElementById("btnAcceder");
  const btnSalir = document.getElementById("btnSalir");

  if (sesion) {
    saludo.textContent = "Hola, " + sesion.nombre;
    saludo.classList.remove("d-none");
    btnAcceder.classList.add("d-none");
    btnSalir.classList.remove("d-none");
  } else {
    saludo.classList.add("d-none");
    btnAcceder.classList.remove("d-none");
    btnSalir.classList.add("d-none");
  }
}

function correoValido(correo) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(correo);
}

document.getElementById("formRegistro").addEventListener("submit", e => {
  e.preventDefault();
  const nombre = document.getElementById("regNombre").value.trim();
  const correo = document.getElementById("regCorreo").value.trim();
  const clave = document.getElementById("regClave").value;
  const mensaje = document.getElementById("mensajeRegistro");

  if (!nombre || !correo || !clave) {
    mostrarMensaje(mensaje, "Completa todos los campos", "danger");
    return;
  }
  if (!correoValido(correo)) {
    mostrarMensaje(mensaje, "El correo no es válido", "danger");
    return;
  }
  if (clave.length < 6) {
    mostrarMensaje(mensaje, "La contraseña debe tener al menos 6 caracteres", "danger");
    return;
  }

  const usuarios = obtenerUsuarios();
  if (usuarios.find(u => u.correo === correo)) {
    mostrarMensaje(mensaje, "Ese correo ya está registrado", "danger");
    return;
  }

  usuarios.push({ nombre: nombre, correo: correo, clave: clave });
  localStorage.setItem("usuarios", JSON.stringify(usuarios));
  document.getElementById("formRegistro").reset();
  mostrarMensaje(mensaje, "Cuenta creada, ahora puedes ingresar", "success");
  bootstrap.Tab.getOrCreateInstance(document.getElementById("tab-login")).show();
});

document.getElementById("formLogin").addEventListener("submit", e => {
  e.preventDefault();
  const correo = document.getElementById("loginCorreo").value.trim();
  const clave = document.getElementById("loginClave").value;
  const mensaje = document.getElementById("mensajeLogin");

  const usuario = obtenerUsuarios().find(u => u.correo === correo && u.clave === clave);
  if (!usuario) {
    mostrarMensaje(mensaje, "Correo o contraseña incorrectos", "danger");
    return;
  }

  localStorage.setItem("sesion", JSON.stringify({ nombre: usuario.nombre, correo: usuario.correo }));
  document.getElementById("formLogin").reset();
  mensaje.innerHTML = "";
  bootstrap.Modal.getOrCreateInstance(document.getElementById("modalAcceso")).hide();
  actualizarSesion();
});

document.getElementById("btnSalir").addEventListener("click", () => {
  localStorage.removeItem("sesion");
  actualizarSesion();
});

document.getElementById("btnConfirmar").addEventListener("click", () => {
  if (carrito.length === 0) {
    mostrarMensaje(mensajeCarrito, "Agrega productos antes de confirmar", "warning");
    return;
  }

  const sesion = obtenerSesion();
  if (!sesion) {
    bootstrap.Offcanvas.getOrCreateInstance(document.getElementById("carrito")).hide();
    bootstrap.Modal.getOrCreateInstance(document.getElementById("modalAcceso")).show();
    return;
  }

  const pedidos = JSON.parse(localStorage.getItem("pedidos")) || [];
  let total = 0;
  carrito.forEach(i => {
    total += i.precio * i.cantidad;
  });
  pedidos.push({ cliente: sesion.correo, items: carrito, total: total });
  localStorage.setItem("pedidos", JSON.stringify(pedidos));

  carrito = [];
  mostrarCarrito();
  mostrarMensaje(mensajeCarrito, "Pedido confirmado, gracias por tu compra", "success");
});

document.getElementById("formContacto").addEventListener("submit", e => {
  e.preventDefault();
  const nombre = document.getElementById("contactoNombre").value.trim();
  const correo = document.getElementById("contactoCorreo").value.trim();
  const texto = document.getElementById("contactoMensaje").value.trim();
  const respuesta = document.getElementById("respuestaContacto");

  if (!nombre || !correo || !texto) {
    mostrarMensaje(respuesta, "Completa todos los campos", "danger");
    return;
  }
  if (!correoValido(correo)) {
    mostrarMensaje(respuesta, "El correo no es válido", "danger");
    return;
  }

  document.getElementById("formContacto").reset();
  mostrarMensaje(respuesta, "Mensaje enviado, te responderemos pronto", "success");
});

mostrarProductos();
mostrarCarrito();
actualizarSesion();