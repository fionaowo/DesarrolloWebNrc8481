const respuestaAPI = {
  status: 200,
  data: [
    { id: 1, nombre: "Completo Italiano", categoria: "Italianos", precio: 2500 },
    { id: 2, nombre: "Italiano Doble", categoria: "Italianos", precio: 3200 },
    { id: 3, nombre: "Completo Dinámico", categoria: "Dinámicos", precio: 2600 },
    { id: 4, nombre: "Dinámico XL", categoria: "Dinámicos", precio: 3400 },
    { id: 5, nombre: "Hot Dog Americano", categoria: "Americanos", precio: 2800 },
    { id: 6, nombre: "Americano Queso", categoria: "Americanos", precio: 3100 }
  ]
};

const filtro = document.getElementById("filtro");
const contenedor = document.getElementById("productos");
const listaPedido = document.getElementById("pedido");
const totalPedido = document.getElementById("total");
let pedido = [];

function crearFiltro() {
  const cmb = document.createElement("select");
  cmb.setAttribute("name", "cmbCategoria");
  cmb.setAttribute("class", "form-select");

  const categorias = ["Todos", ...new Set(respuestaAPI.data.map(p => p.categoria))];
  categorias.forEach(cat => {
    const opt = document.createElement("option");
    opt.setAttribute("value", cat);
    opt.innerText = cat;
    cmb.appendChild(opt);
  });

  cmb.addEventListener("change", () => mostrarProductos(cmb.value));
  filtro.appendChild(cmb);
}

function mostrarProductos(categoria) {
  contenedor.innerHTML = "";
  const lista = categoria === "Todos"
    ? respuestaAPI.data
    : respuestaAPI.data.filter(p => p.categoria === categoria);

  lista.forEach(prod => {
    const col = document.createElement("div");
    col.setAttribute("class", "col-12 col-sm-6 mb-3");

    const card = document.createElement("div");
    card.setAttribute("class", "card h-100");

    const body = document.createElement("div");
    body.setAttribute("class", "card-body");

    const titulo = document.createElement("h5");
    titulo.innerText = prod.nombre;

    const precio = document.createElement("p");
    precio.innerText = "$" + prod.precio;

    const btnAgregar = document.createElement("button");
    btnAgregar.setAttribute("class", "btn btn-warning me-2");
    btnAgregar.innerText = "Agregar";
    btnAgregar.addEventListener("click", () => agregar(prod));

    const btnDetalle = document.createElement("button");
    btnDetalle.setAttribute("class", "btn btn-outline-dark");
    btnDetalle.innerText = "Detalle";
    btnDetalle.addEventListener("click", () => mostrarDetalle(prod, body));

    body.appendChild(titulo);
    body.appendChild(precio);
    body.appendChild(btnAgregar);
    body.appendChild(btnDetalle);
    card.appendChild(body);
    col.appendChild(card);
    contenedor.appendChild(col);
  });
}

function mostrarDetalle(prod, body) {
  const anterior = body.querySelector("ul");
  if (anterior) {
    body.removeChild(anterior);
    return;
  }

  const ul = document.createElement("ul");
  ul.setAttribute("class", "mt-2");
  Object.entries(prod).forEach(([clave, valor]) => {
    const li = document.createElement("li");
    li.innerText = clave + ": " + valor;
    ul.appendChild(li);
  });
  body.appendChild(ul);
}

function agregar(prod) {
  const existente = pedido.find(i => i.id === prod.id);

  if (existente) {
    existente.cantidad++;
  } else {
    const item = Object.assign({}, prod, { cantidad: 1 });
    delete item.categoria;
    pedido.push(item);
  }

  mostrarPedido();
}

function mostrarPedido() {
  listaPedido.innerHTML = "";

  pedido.forEach(item => {
    const li = document.createElement("li");
    li.setAttribute("class", "list-group-item d-flex justify-content-between align-items-center");
    li.innerText = item.cantidad + " x " + item.nombre + " - $" + item.precio * item.cantidad;

    const btnQuitar = document.createElement("button");
    btnQuitar.setAttribute("class", "btn btn-sm btn-danger");
    btnQuitar.innerText = "Quitar";
    btnQuitar.addEventListener("click", () => {
      pedido = pedido.filter(i => i.id !== item.id);
      listaPedido.removeChild(li);
      actualizarTotal();
    });

    li.appendChild(btnQuitar);
    listaPedido.appendChild(li);
  });

  actualizarTotal();
}

function actualizarTotal() {
  let total = 0;
  pedido.forEach(item => {
    total += item.precio * item.cantidad;
  });
  totalPedido.innerText = total;
}

crearFiltro();
mostrarProductos("Todos");