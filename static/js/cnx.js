document.addEventListener("DOMContentLoaded", function () {
    // ✅ قراءة CSRF token من الmeta tag
    const csrftoken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    // ✅ التحقق مما إذا كان المستخدم متصلاً
    fetch("/dashboard/", {
        method: "GET",
        headers: {
            "X-Requested-With": "XMLHttpRequest"
        }
    })
    .then(response => {
        if (response.redirected) {
            window.location.href = response.url; // 🔄 إعادة التوجيه إلى صفحة تسجيل الدخول
        }
    })
    .catch(error => console.error("❌ خطأ في التحقق من الجلسة:", error));

    // ✅ تسجيل الخروج عند النقر على زر "Déconnexion"
    const logoutButton = document.getElementById("logout");
    if (logoutButton) {
        logoutButton.addEventListener("click", function (event) {
            event.preventDefault();
            fetch("/logout/", {
                method: "POST",
                credentials: "same-origin",
                headers: {
                    "X-CSRFToken": csrftoken, // 🔥 نرسل CSRF Token هنا
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
            .then(response => {
                if (response.redirected) {
                    window.location.href = response.url; // 🔄 إعادة التوجيه بعد تسجيل الخروج
                }
            })
            .catch(error => console.error("❌ خطأ أثناء تسجيل الخروج:", error));
        });
    }
});
