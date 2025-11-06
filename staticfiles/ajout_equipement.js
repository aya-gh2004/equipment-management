document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("ajoutMachineForm");
    const messageSuccess = document.getElementById("messageSuccess");
    const qrCodeContainer = document.getElementById("qrCodeContainer");
    const qrCodeDiv = document.getElementById("qrCode");

    form.addEventListener("submit", function (event) {
        event.preventDefault();

        let nom = document.getElementById("nom").value.trim();
        let type = document.getElementById("type").value.trim();
        let numero = document.getElementById("numero").value.trim();
        let marque = document.getElementById("marque").value.trim();
        let modele = document.getElementById("modele").value.trim();
        let dateAchat = document.getElementById("dateAchat").value;
        let etat = document.getElementById("etat").value;
        let emplacement = document.getElementById("emplacement").value.trim();
        let responsable = document.getElementById("responsable").value.trim();
        let codeQR = document.getElementById("codeQR").value.trim();

        if (nom === "" || type === "" || numero === "") {
            alert("Veuillez remplir les champs obligatoires !");
            return;
        }

        let machine = {
            name: nom,
            category: type,
            serial_number: numero,
            brand: marque,
            model: modele,
            purchase_date: dateAchat,
            status: etat,
            location: emplacement,
            responsible: responsable,
            qr_code: codeQR || `Nom: ${nom}\nType: ${type}\nNuméro: ${numero}\nMarque: ${marque}\nModèle: ${modele}`
        };

        envoyerMachineDjango(machine);
    });

    function envoyerMachineDjango(machine) {
        const csrftoken = getCSRFToken();

        fetch("/api/equipment/add/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken
            },
            body: JSON.stringify(machine)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                messageSuccess.classList.remove("hidden");
                genererQRCode(machine.qr_code);
                form.reset();

                setTimeout(() => {
                    messageSuccess.classList.add("hidden");
                }, 3000);
            } else {
                alert("Erreur lors de l'ajout de la machine !");
            }
        })
        .catch(error => {
            console.error("Erreur:", error);
            alert("Une erreur est survenue !");
        });
    }

    function genererQRCode(texte) {
        qrCodeDiv.innerHTML = "";
        new QRCode(qrCodeDiv, {
            text: texte,
            width: 200,
            height: 200
        });

        qrCodeContainer.classList.remove("hidden");
    }

    function getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }
});
