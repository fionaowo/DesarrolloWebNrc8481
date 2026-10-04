<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
  <div class="container-fluid">
    <a class="navbar-brand" href="index.php">Doggy's</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#menuPrincipal">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="menuPrincipal">
      <ul class="navbar-nav me-auto">
        <li class="nav-item"><a class="nav-link" href="index.php">Inicio</a></li>
        <li class="nav-item"><a class="nav-link" href="empresa.php">Empresa</a></li>
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" data-bs-toggle="dropdown">Productos</a>
          <ul class="dropdown-menu">
            <li><a class="dropdown-item" href="productos.php">Todos</a></li>
            <li><a class="dropdown-item" href="productos.php?cat=Italianos">Italianos</a></li>
            <li><a class="dropdown-item" href="productos.php?cat=Dinámicos">Dinámicos</a></li>
            <li><a class="dropdown-item" href="productos.php?cat=Americanos">Americanos</a></li>
          </ul>
        </li>
        <li class="nav-item"><a class="nav-link" href="contacto.php">Contacto</a></li>
      </ul>
      <button class="btn btn-outline-warning" data-bs-toggle="modal" data-bs-target="#modalLogin">Acceder</button>
    </div>
  </div>
</nav>

<div class="modal fade" id="modalLogin" tabindex="-1">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Iniciar sesión</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <div class="modal-body">
        <form action="index.php" method="POST">
          <input type="email" name="correo" class="form-control mb-2" placeholder="Correo" required>
          <input type="password" name="clave" class="form-control mb-2" placeholder="Contraseña" required>
          <button type="submit" class="btn btn-warning w-100">Ingresar</button>
        </form>
      </div>
    </div>
  </div>
</div>