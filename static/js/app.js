let editMode = false;
let deleteId = null;

async function fetchCredits() {
    const res = await fetch("/api/creditos");
    const data = await res.json();
    const tbody = document.getElementById("creditsTable");
    tbody.innerHTML = "";
    data.forEach(c => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
      <td style='display: none'>${c.id}</td>
      <td>${c.cliente}</td>
      <td>$${c.monto.toFixed(2)}</td>
      <td>${c.tasa_interes}%</td>
      <td>${c.plazo}</td>
      <td>${c.fecha_otorgamiento}</td>
      <td>
        <button class='btn btn-primary' onclick='openModal(true, ${JSON.stringify(c)})'>
          Editar
        </button>
        <button class='btn btn-danger' onclick="openConfirmModal(${c.id})">
          Eliminar
        </button>
      </td>
    `;
        tbody.appendChild(tr);
    });
}
function openConfirmModal(id) {
  deleteId = id;
  document.getElementById("confirmModal").classList.remove("hidden");
}

function closeConfirmModal() {
  deleteId = null;
  document.getElementById("confirmModal").classList.add("hidden");
}

document.getElementById("confirmDeleteBtn").addEventListener("click", async () => {
  if (!deleteId) return;
  const res = await fetch(`/api/creditos/${deleteId}`, { method: "DELETE" });
  if (res.ok) {
    console.log("Crédito eliminado");
    closeConfirmModal();
    await fetchCredits();
    await fetchSummary();
  } else {
    alert("❌ Error al eliminar el crédito");
  }
});

// Modal helpers
function openModal(isEdit = false, credit = null) {
    const modal = document.getElementById("modal");
    const title = document.getElementById("modalTitle");
    const form = document.getElementById("creditForm");

    editMode = isEdit;
    modal.classList.remove("hidden");
    modal.classList.add("flex");

    if (isEdit && credit) {
        title.textContent = "Editar Crédito";
        form.id.value = credit.id;
        form.cliente.value = credit.cliente;
        form.monto.value = credit.monto;
        form.tasa_interes.value = credit.tasa_interes;
        form.plazo.value = credit.plazo;
        form.fecha_otorgamiento.value = credit.fecha_otorgamiento;

        // Deshabilitar fecha en edición
        form.fecha_otorgamiento.disabled = true;
    } else {
        title.textContent = "Registrar Crédito";
        clearForm();
        form.fecha_otorgamiento.disabled = false;
    }
}

function closeModal() {
    const modal = document.getElementById("modal");
    modal.classList.add("hidden");
    modal.classList.remove("flex");
    clearForm();
}

function clearForm() {
    const form = document.getElementById("creditForm");
    form.reset();
    form.id.value = "";
    form.fecha_otorgamiento.disabled = false;
}

// Registrar o Editar crédito
document.getElementById("creditForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const form = e.target;
    const formData = new FormData(form);
    const json = Object.fromEntries(formData.entries());

    json.monto = parseFloat(json.monto);
    json.tasa_interes = parseFloat(json.tasa_interes);
    json.plazo = parseInt(json.plazo);

    if (editMode) {
        // Editar crédito
        await fetch(`/api/creditos/${json.id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(json)
        });
    } else {
        // Crear crédito
        await fetch("/api/creditos", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(json)
        });
    }

    closeModal();
    await fetchCredits();
    await fetchSummary();
});


// Chart.js
let chart;
const floatRegex = /^\d+(\.\d{1,2})?$/;

async function fetchSummary(min = null, max = null) {
    let url = "api/creditos/statistics";
    const params = [];
    if (min !== null) params.push(`min=${min}`);
    if (max !== null) params.push(`max=${max}`);
    if (params.length) url += "?" + params.join("&");

    const res = await fetch(url);
    const data = await res.json();

    // actualizar labels
    document.getElementById("totalCreditos").textContent = data.total_count;
    document.getElementById("totalMonto").textContent = "$" + data.total_monto.toLocaleString();

    const ctx = document.getElementById("summaryChart").getContext("2d");
    const labels = data.por_cliente.map(c => c.cliente);
    const values = data.por_cliente.map(c => c.total);
    const counts = data.por_cliente.map(c => c.count);

    if (chart) chart.destroy();
    chart = new Chart(ctx, {
        type: "bar",
        data: {
            labels,
            datasets: [{
                label: "Monto total por cliente",
                data: values,
                backgroundColor: "#2563eb"
            }]
        },
        options: {
            layout: {
                padding: {
                    top: 30,
                    bottom: 10,
                    left: 10,
                    right: 10
                }
            },
            responsive: true,
            plugins: {
                legend: {
                    position: "bottom"
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            let idx = context.dataIndex;
                            let monto = values[idx].toLocaleString();
                            let numCreditos = counts[idx];
                            return `Monto: $${monto} (No. de créditos: ${numCreditos})`;
                        }
                    }
                },
                datalabels: {
                    anchor: "end",
                    align: "end",
                    formatter: (value, ctx) => counts[ctx.dataIndex] + " créditos"
                }
            }
        },
        plugins: [ChartDataLabels]
    });
}

// Aplicar filtros
function applyFilters() {
    const minInput = document.getElementById("minMonto");
    const maxInput = document.getElementById("maxMonto");
    const minError = document.getElementById("minMonto-error");
    const maxError = document.getElementById("maxMonto-error");

    const minVal = minInput.value.trim();
    const maxVal = maxInput.value.trim();

    let valid = true;

    // reset
    minError.classList.remove("show");
    maxError.classList.remove("show");
    minInput.classList.remove("input-error");
    maxInput.classList.remove("input-error");

    // validar flotante o vacío
    if (minVal && !floatRegex.test(minVal)) {
        minError.classList.add("show");
        minInput.classList.add("input-error");
        valid = false;
    }
    if (maxVal && !floatRegex.test(maxVal)) {
        maxError.classList.add("show");
        maxInput.classList.add("input-error");
        valid = false;
    }

    // validar rango lógico (si ambos existen)
    if (minVal && maxVal && parseFloat(minVal) > parseFloat(maxVal)) {
        maxError.textContent = "El máximo debe ser mayor o igual al mínimo.";
        maxError.classList.add("show");
        maxInput.classList.add("input-error");
        valid = false;
    } else {
        // reset mensaje si vuelve a estar correcto
        maxError.textContent =
            "Ingrese un número válido con máximo 2 decimales.";
    }

    if (!valid) return; // no continuar si hay errores

    fetchSummary(minVal || null, maxVal || null);
}

// Captura submit del formulario de filtros
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("chartForm");
    form.addEventListener("submit", (e) => {
        e.preventDefault();
        applyFilters();
    });

    // cargar datos iniciales sin filtros
    fetchSummary();
});

// Inicialización
fetchCredits();
fetchSummary();
