const ctx = document.getElementById('myChart');
let teste = document.getElementById('teste');

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
      datasets: [{
        label: '# of Votes',
        data: [12, 19, 3, 5, 2, 3],
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });

  // Função para menu no aside
function toggleMenu(menuId) {
    var submenu = document.getElementById(menuId);
    if (submenu.style.display === "none" || submenu.style.display === "") {
        submenu.style.display = "block";
    } else {
        submenu.style.display = "none";
    }
}

document.addEventListener("DOMContentLoaded", function() {
  fetch('/dados-settlements')  
      .then(response => response.json())
      .then(data => {
          let tbody = document.querySelector("#table tbody");
          tbody.innerHTML = "";
          
          data.forEach(item => {
              let row = `<tr>
                  <td>${item.total_sales}</td>
                  <td>${item.orders}</td>
                  <td>${item.avg_delivery}</td>
                  <td>${item.ratings}</td>
              </tr>`;
              tbody.innerHTML += row;
          });
      })
      .catch(error => console.error('Erro ao buscar dados:', error));
});


fetch('/dados-settlements')  
    .then(response => response.json())
    .then(data => {
        document.querySelector(".card.total p").innerHTML = `R$ ${data.total_sales} Total<br>R$ ${data.product_sales} Produtos`;
        document.querySelector(".card.orders p").innerHTML = `${data.orders} Pedidos<br>R$ ${data.avg_ticket} Ticket Médio`;
        document.querySelector(".card.delivery p").innerHTML = `R$ ${data.avg_delivery} Entrega Média`;
        document.querySelector(".card.ratings p").innerHTML = `${data.ratings_count} Avaliações<br>${data.avg_rating} Nota Média`;
    })
    .catch(error => console.error('Erro ao buscar dados:', error));




    document.addEventListener("DOMContentLoaded", function() {
      const mockData = [
          { total_sales: "70.093,41", orders: 1123, avg_delivery: "3,42", ratings: 4.8 },
          { total_sales: "60.100,41", orders: 2500, avg_delivery: "10,42", ratings: 5.0 }
      ];
  
      let tbody = document.getElementById("table-body");
      tbody.innerHTML = "";
  
      mockData.forEach(item => {
          let row = `<tr>
              <td>R$ ${item.total_sales}</td>
              <td>${item.orders}</td>
              <td>R$ ${item.avg_delivery}</td>
              <td>${item.ratings}</td>
          </tr>`;
          tbody.innerHTML += row;
      });
  
      const latestData = mockData[0]; 
  
      document.getElementById("total-sales").innerHTML = `R$ ${latestData.total_sales} Total<br>R$ 67.358,74 Produtos`;
      document.getElementById("total-orders").innerHTML = `${latestData.orders} Pedidos<br>R$ 62,42 Ticket Médio`;
      document.getElementById("avg-delivery").innerHTML = `R$ ${latestData.avg_delivery} Entrega Média`;
      document.getElementById("avg-rating").innerHTML = `41 Avaliações<br>${latestData.ratings} Nota Média`;
  });
  