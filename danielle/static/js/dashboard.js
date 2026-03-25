document.addEventListener("DOMContentLoaded", function () {
  // debug: verificar se elementos JSON existem
  console.log("=== DEBUG DASHBOARD ===");

  const reasonsDataElement = document.getElementById("reasons-data");
  const reasonsValuesElement = document.getElementById("reasons-values");
  const servicesLabelsElement = document.getElementById("services-labels");
  const servicesValuesElement = document.getElementById("services-values");

  console.log("Elementos encontrados:", {
    "reasons-data": reasonsDataElement,
    "reasons-values": reasonsValuesElement,
    "services-labels": servicesLabelsElement,
    "services-values": servicesValuesElement,
  });

  // verificar se todos elementos existem
  if (
    !reasonsDataElement ||
    !reasonsValuesElement ||
    !servicesLabelsElement ||
    !servicesValuesElement
  ) {
    console.error("Elementos JSON não encontrados no template!");
    return;
  }

  // tentar fazer parse dos dados
  try {
    let reasonsLabels = JSON.parse(reasonsDataElement.textContent);
    let reasonsValues = JSON.parse(reasonsValuesElement.textContent);
    let servicesLabels = JSON.parse(servicesLabelsElement.textContent);
    let servicesValues = JSON.parse(servicesValuesElement.textContent);

    // fazer segundo parse pois dados vêm com double encoding
    reasonsLabels = JSON.parse(reasonsLabels);
    reasonsValues = JSON.parse(reasonsValues);
    servicesLabels = JSON.parse(servicesLabels);
    servicesValues = JSON.parse(servicesValues);

    console.log("Dados parseados (após double parse):", {
      reasonsLabels,
      reasonsValues,
      servicesLabels,
      servicesValues,
    });

    // verificar se são arrays válidos
    if (!Array.isArray(reasonsLabels) || !Array.isArray(reasonsValues)) {
      console.error("Dados de reasons não são arrays válidos!");
      return;
    }

    if (!Array.isArray(servicesLabels) || !Array.isArray(servicesValues)) {
      console.error("Dados de services não são arrays válidos!");
      return;
    }

    // criar gráficos apenas se dados válidos
    initReasonsChart(reasonsLabels, reasonsValues);
    initServicesChart(servicesLabels, servicesValues);
  } catch (error) {
    console.error("Erro ao fazer parse do JSON:", error);
  }
});

// gráfico pizza: perfil de check-ins
function initReasonsChart(labels, values) {
  console.log("Criando gráfico reasons com:", labels, values);

  const ctx = document.getElementById("reasonsChart").getContext("2d");

  new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: labels,
      datasets: [
        {
          data: values,
          backgroundColor: [
            "#FF6B6B",
            "#4ECDC4",
            "#45B7D1",
            "#96CEB4",
            "#FFEAA7",
            "#DDA0DD",
          ],
          borderWidth: 3,
          borderColor: "#ffffff",
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: true,
          position: "bottom",
        },
      },
    },
  });
}

// gráfico barras: serviços
let servicesChart;
function initServicesChart(labels, values) {
  console.log("Criando gráfico services com:", labels, values);

  const ctx = document.getElementById("servicesChart").getContext("2d");

  const config = {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Quantidade",
          data: values,
          backgroundColor: [
            "rgba(54, 162, 235, 0.6)",
            "rgba(255, 206, 86, 0.6)",
            "rgba(75, 192, 192, 0.6)",
            "rgba(153, 102, 255, 0.6)",
            "rgba(255, 159, 64, 0.6)",
            "rgba(255, 99, 132, 0.6)",
          ],
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: { y: { beginAtZero: true } },
      plugins: { legend: { display: false } },
    },
  };

  servicesChart = new Chart(ctx, config);
}

// alterar tipo do gráfico de serviços
function updateChartType(newType) {
  if (servicesChart) {
    servicesChart.destroy();
  }

  // double parse devido ao double encoding
  let labels = JSON.parse(
    document.getElementById("services-labels").textContent,
  );
  let values = JSON.parse(
    document.getElementById("services-values").textContent,
  );
  labels = JSON.parse(labels);
  values = JSON.parse(values);

  const ctx = document.getElementById("servicesChart").getContext("2d");
  const config = {
    type: newType,
    data: {
      labels: labels,
      datasets: [
        {
          label: "Quantidade",
          data: values,
          backgroundColor: [
            "rgba(54, 162, 235, 0.6)",
            "rgba(255, 206, 86, 0.6)",
            "rgba(75, 192, 192, 0.6)",
            "rgba(153, 102, 255, 0.6)",
            "rgba(255, 159, 64, 0.6)",
            "rgba(255, 99, 132, 0.6)",
          ],
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: { y: { beginAtZero: true } },
      plugins: { legend: { display: newType === "polarArea" } },
    },
  };

  servicesChart = new Chart(ctx, config);
}
