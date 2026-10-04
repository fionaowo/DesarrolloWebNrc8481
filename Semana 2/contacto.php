<?php
$titulo = "Contacto";
include "head.php";
include "navbar.php";

$mensaje = "";
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $nombre = htmlspecialchars($_POST["nombre"]);
    $mensaje = "Gracias por escribirnos, " . $nombre . ". Te responderemos pronto.";
}
?>

<div class="container mt-4">
  <div class="row">
    <div class="col-12 col-md-6">
      <h2>Contáctanos</h2>
      <?php if ($mensaje != "") { ?>
        <div class="alert alert-success"><?php echo $mensaje; ?></div>
      <?php } ?>
      <form action="contacto.php" method="POST">
        <div class="mb-3">
          <label class="form-label">Nombre</label>
          <input type="text" name="nombre" class="form-control" required>
        </div>
        <div class="mb-3">
          <label class="form-label">Correo</label>
          <input type="email" name="correo" class="form-control" required>
        </div>
        <div class="mb-3">
          <label class="form-label">Mensaje</label>
          <textarea name="mensaje" class="form-control" rows="4" required></textarea>
        </div>
        <button type="submit" class="btn btn-warning">Enviar</button>
      </form>
    </div>
    <div class="col-12 col-md-6">
      <h4>Datos del local</h4>
      <p>Teléfono: +56 9 1234 5678</p>
      <p>Correo: hola@doggys.cl</p>
      <p>Horario: lunes a domingo, 11:00 a 23:30</p>
    </div>
  </div>
</div>

<?php include "footer.php"; ?>