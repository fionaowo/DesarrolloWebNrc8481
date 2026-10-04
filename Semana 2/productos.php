<?php
$titulo = "Productos";
include "datos.php";
include "head.php";
include "navbar.php";

$cat = isset($_GET["cat"]) ? $_GET["cat"] : "Todos";
?>

<div class="container mt-4">
  <h2 class="mb-3">Nuestros productos</h2>
  <div class="mb-3">
    <a href="productos.php" class="btn btn-outline-dark btn-sm">Todos</a>
    <a href="productos.php?cat=Italianos" class="btn btn-outline-dark btn-sm">Italianos</a>
    <a href="productos.php?cat=Dinámicos" class="btn btn-outline-dark btn-sm">Dinámicos</a>
    <a href="productos.php?cat=Americanos" class="btn btn-outline-dark btn-sm">Americanos</a>
  </div>
  <div class="row">
    <?php foreach ($productos as $p) {
      if ($cat == "Todos" || $p["categoria"] == $cat) { ?>
        <div class="col-12 col-sm-6 col-lg-4 mb-3">
          <div class="card h-100">
            <img src="<?php echo $p['img']; ?>" class="card-img-top" style="height:200px; object-fit:cover;" alt="<?php echo $p['nombre']; ?>">
            <div class="card-body">
              <span class="badge bg-warning text-dark"><?php echo $p['categoria']; ?></span>
              <h5 class="card-title mt-2"><?php echo $p['nombre']; ?></h5>
              <p class="card-text"><?php echo $p['desc']; ?></p>
              <p class="fw-bold text-danger">$<?php echo number_format($p['precio'], 0, ',', '.'); ?></p>
            </div>
          </div>
        </div>
    <?php }
    } ?>
  </div>
</div>

<?php include "footer.php"; ?>