function toggleContenido() {


  const miDiv = document.querySelector('[data-target="bodyContainer"]');
  

  const estaExpandido = miDiv.classList.contains('expandable__expanded');

  if (estaExpandido) {

    // Acciones para ocultar
    miDiv.classList.remove('expandable__expanded');
    miDiv.setAttribute('data-testid', 'VTC7M0-benefits-description-hidden');
    miDiv.style.maxHeight = '0px';
  } else {

    // Acciones para mostrar
    miDiv.classList.add('expandable__expanded');
    miDiv.setAttribute('data-testid', 'VTC7M0-benefits-description-visible');
    
    // Nota: A veces '100vh' hace que se vea mal o salte la pantalla. 
    // Usar un valor en píxeles grande (como 1000px) suele dar una animación más fluida.
    miDiv.style.maxHeight = '1000px'; 
  }
}