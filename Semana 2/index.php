<?php
$titulo = "Inicio";
include "datos.php";
include "head.php";
include "navbar.php";
?>

<div id="carruselDoggys" class="carousel slide" data-bs-ride="carousel">
  <div class="carousel-indicators">
    <button type="button" data-bs-target="#carruselDoggys" data-bs-slide-to="0" class="active"></button>
    <button type="button" data-bs-target="#carruselDoggys" data-bs-slide-to="1"></button>
    <button type="button" data-bs-target="#carruselDoggys" data-bs-slide-to="2"></button>
  </div>
  <div class="carousel-inner">
    <div class="carousel-item active">
      <img src="https://images.pexels.com/photos/4113472/pexels-photo-4113472.jpeg?auto=compress&cs=tinysrgb&w=1200" class="d-block w-100" style="height:400px; object-fit:cover;" alt="Hot dogs">
      <div class="carousel-caption">
        <h2>Completos 100% naturales</h2>
        <p>Ingredientes frescos todos los días</p>
      </div>
    </div>
    <div class="carousel-item">
      <img src="https://images.pexels.com/photos/4113458/pexels-photo-4113458.jpeg?auto=compress&cs=tinysrgb&w=1200" class="d-block w-100" style="height:400px; object-fit:cover;" alt="Combo">
      <div class="carousel-caption">
        <h2>Combo Doble</h2>
        <p>Dos hot dogs, papas y dos bebidas</p>
      </div>
    </div>
    <div class="carousel-item">
      <img src="https://images.pexels.com/photos/4113504/pexels-photo-4113504.jpeg?auto=compress&cs=tinysrgb&w=1200" class="d-block w-100" style="height:400px; object-fit:cover;" alt="Italiano">
      <div class="carousel-caption">
        <h2>El clásico italiano</h2>
        <p>Tomate, palta y mayonesa</p>
      </div>
    </div>
  </div>
  <button class="carousel-control-prev" type="button" data-bs-target="#carruselDoggys" data-bs-slide="prev">
    <span class="carousel-control-prev-icon"></span>
  </button>
  <button class="carousel-control-next" type="button" data-bs-target="#carruselDoggys" data-bs-slide="next">
    <span class="carousel-control-next-icon"></span>
  </button>
</div>

<div class="container mt-4">
  <h2 class="text-center mb-4">Productos destacados</h2>
  <div class="row">
    <?php foreach (array_slice($productos, 0, 3) as $p) { ?>
      <div class="col-12 col-md-4 mb-3">
        <div class="card h-100">
          <img src="<?php echo $p['img']; ?>" class="card-img-top" style="height:200px; object-fit:cover;" alt="<?php echo $p['nombre']; ?>">
          <div class="card-body">
            <h5 class="card-title"><?php echo $p['nombre']; ?></h5>
            <p class="card-text"><?php echo $p['desc']; ?></p>
            <p class="fw-bold text-danger">$<?php echo number_format($p['precio'], 0, ',', '.'); ?></p>
          </div>
        </div>
      </div>
    <?php } ?>
  </div>
  <div class="text-center">
    <a href="productos.php" class="btn btn-warning">Ver todos los productos</a>
  </div>
</div>

<?php include "footer.php"; ?>