document.addEventListener("DOMContentLoaded", function () {
    const notificationForm = document.getElementById("notificationForm");
    const notificationList = document.getElementById("notificationList");

    // Notifications initiales (peut être connecté à un backend plus tard)
    const initialNotifications = [
        { message: "Mise à jour système à 18h.", type: "info" },
        { message: "Incident sur la ligne de production 3.", type: "alerte" }
    ];

    initialNotifications.forEach(notif => addNotification(notif.message, notif.type));

    notificationForm.addEventListener("submit", function (e) {
        e.preventDefault();
        const message = document.getElementById("notificationText").value;
        const type = document.getElementById("notificationType").value;
        addNotification(message, type);
        notificationForm.reset();
    });

    function addNotification(message, type) {
        const li = document.createElement("li");
        li.classList.add(type);

        li.innerHTML = `
            <span>${message}</span>
            <button class="btn-delete">🗑️</button>
        `;

        li.querySelector(".btn-delete").onclick = () => li.remove();
        notificationList.appendChild(li);
    }
});

// Fonction pour montrer/cacher la sidebar
function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    const mainContent = document.querySelector('.main-content');
    if (sidebar.style.width === '0px' || sidebar.style.width === '') {
        sidebar.style.width = '250px';
        mainContent.style.marginLeft = '250px';
    } else {
        sidebar.style.width = '0';
        mainContent.style.marginLeft = '0';
    }
}
