document.addEventListener("DOMContentLoaded", function () {
    fetch("/api/statistiques//api")
        .then(response => {
            if (!response.ok) {
                throw new Error("Erreur HTTP " + response.status);
            }
            return response.json();
        })
        .then(data => {
            console.log("Données récupérées :", data);

            const total = data.total || 0;
            const enPanne = data.en_panne || 0;
            const enMaintenance = data.en_maintenance || 0;
            const enService = total - enPanne - enMaintenance;

            // Mise à jour des cartes HTML
            document.getElementById("totalEquipments").textContent = total;
            document.getElementById("brokenEquipments").textContent = enPanne;
            document.getElementById("maintenanceEquipments").textContent = enMaintenance;
            document.getElementById("fonctionnementEquipments").textContent = enService;

            // Diagramme en barres
            new Chart(document.getElementById("barChart"), {
                type: "bar",
                data: {
                    labels: ["En foctionnement", "En panne", "En maintenance"],
                    datasets: [{
                        label: "Nombre d'équipements",
                        data: [enService, enPanne, enMaintenance],
                        backgroundColor: ["#00c853", "#ff5252", "#ffca28"]
                    }]
                }
            });

            // Diagramme circulaire
            new Chart(document.getElementById("pieChart"), {
                type: "pie",
                data: {
                    labels: ["En foctionnement", "En panne", "En maintenance"],
                    datasets: [{
                        data: [enService, enPanne, enMaintenance],
                        backgroundColor: ["#00c853", "#ff5252", "#ffca28"]
                    }]
                }
            });

            // Diagramme linéaire
            new Chart(document.getElementById("lineChart"), {
                type: "line",
                data: {
                    labels: ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin"],
                    datasets: [{
                        label: "Évolution du total",
                        data: [total - 10, total - 8, total - 5, total - 3, total, total + 2],
                        borderColor: "#007BFF",
                        fill: false
                    }]
                }
            });
        })
        .catch(error => {
            console.error("Erreur lors du chargement des statistiques :", error);
        });
});

// Gestion de l'upload de fichier
function uploadFile() {
    const file = document.getElementById("fileInput").files[0];
    if (!file) {
        alert("Veuillez sélectionner un fichier !");
        return;
    }
    const li = document.createElement("li");
    li.textContent = file.name;
    document.getElementById("fileList").appendChild(li);
}

// Toggle sidebar
function toggleMenu() {
    document.getElementById("sidebar").classList.toggle("collapsed");
}
