
  /********************************
  ***** CODIGO DEL SIDEBAR*********
  *********************************
  *********************************/
 
  document.addEventListener('DOMContentLoaded', () => {
    const menuIcon = document.querySelector('.menu-icon');
    const sidebar = document.getElementById('sidebar');
    const closeBtn = document.getElementById('close-sidebar');
  
    menuIcon.addEventListener('click', () => {
      sidebar.classList.add('open');
    });
  
    closeBtn.addEventListener('click', () => {
      sidebar.classList.remove('open');
    });
  
    // Cerrar si se hace clic fuera del sidebar
    document.addEventListener('click', (event) => {
      if (
        sidebar.classList.contains('open') &&
        !sidebar.contains(event.target) &&
        !menuIcon.contains(event.target)
      ) {
        sidebar.classList.remove('open');
      }
    });
  });
  