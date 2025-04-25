document.addEventListener("DOMContentLoaded", () => {
    const monthNames = [
      "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
      "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ];
  
    const calendarBody = document.getElementById("calendar-body");
    const monthNameElement = document.getElementById("month-name");
    const yearElement = document.getElementById("year");
    const prevMonthButton = document.getElementById("prev-month");
    const nextMonthButton = document.getElementById("next-month");
  
    let currentDate = new Date();
  
    function renderCalendar(date) {
      const year = date.getFullYear();
      const month = date.getMonth();
  
      // Actualizar el encabezado del mes y año
      monthNameElement.textContent = monthNames[month];
      yearElement.textContent = year;
  
      // Obtener el primer día del mes
      const firstDay = new Date(year, month, 1).getDay();
      const daysInMonth = new Date(year, month + 1, 0).getDate();
  
      // Limpiar el cuerpo del calendario
      calendarBody.innerHTML = "";
  
      // Crear las filas y celdas del calendario
      let row = document.createElement("tr");
      for (let i = 0; i < (firstDay === 0 ? 6 : firstDay - 1); i++) {
        const emptyCell = document.createElement("td");
        row.appendChild(emptyCell);
      }
  
      for (let day = 1; day <= daysInMonth; day++) {
        if (row.children.length === 7) {
          calendarBody.appendChild(row);
          row = document.createElement("tr");
        }
  
        const cell = document.createElement("td");
        cell.textContent = day;
  
        // Resaltar los domingos
        if ((row.children.length + 1) % 7 === 0) {
          cell.classList.add("highlight-red");
        }
  
        row.appendChild(cell);
      }
  
      // Agregar la última fila
      if (row.children.length > 0) {
        calendarBody.appendChild(row);
      }
    }
  
    // Navegar entre meses
    prevMonthButton.addEventListener("click", () => {
      currentDate.setMonth(currentDate.getMonth() - 1);
      renderCalendar(currentDate);
    });
  
    nextMonthButton.addEventListener("click", () => {
      currentDate.setMonth(currentDate.getMonth() + 1);
      renderCalendar(currentDate);
    });
  
    // Renderizar el calendario inicial
    renderCalendar(currentDate);
  });



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
  