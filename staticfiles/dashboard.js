document.addEventListener("DOMContentLoaded", function () {
    // ✅ التحكم في الشريط الجانبي (Sidebar)
    const sidebar = document.getElementById("sidebar");
    const menuToggle = document.getElementById("menuToggle");
    const mainContent = document.querySelector(".main-content");

    if (menuToggle && sidebar && mainContent) {
        menuToggle.addEventListener("click", () => {
            const isSidebarOpen = sidebar.style.left === "0px";
            sidebar.style.left = isSidebarOpen ? "-250px" : "0px";
            mainContent.style.marginLeft = isSidebarOpen ? "0" : "250px";
        });
    } else {
        console.warn("⚠️ Élément du menu latéral non trouvé !");
    }

    // ✅ رسائل عند الضغط على الأزرار
    const buttonMessages = {
        btnTotal: "🛠️ Affichage des équipements !",
        btnPanne: "⚠️ Liste des machines en panne !",
        btnMaintenance: "🔧 Machines en maintenance !",
        btnOperationnel: "✅ Machines opérationnelles !",
        btnUsers: "👥 Liste des utilisateurs !"
    };

    for (const [id, message] of Object.entries(buttonMessages)) {
        const button = document.getElementById(id);
        if (button) {
            button.addEventListener("click", () => alert(message));
        } else {
            console.warn(`⚠️ Bouton ${id} non trouvé !`);
        }
    }
});
