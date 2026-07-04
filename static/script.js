document.addEventListener("DOMContentLoaded", () => {

    // ---------------- ASK NOTIFICATION PERMISSION ----------------

    if ("Notification" in window) {

        if (Notification.permission !== "granted") {

            Notification.requestPermission();

        }

    }

    // ---------------- GET TASKS ----------------

    const taskCards = document.querySelectorAll(".task-card");

    taskCards.forEach(card => {

        const dueElement = card.querySelector(".due-time");

        if (!dueElement) return;

        const dueRaw = dueElement.dataset.raw;

        if (!dueRaw) return;

        const dueDate = new Date(dueRaw);

        const now = new Date();

        const diffMs = dueDate - now;

        const diffHours = diffMs / (1000 * 60 * 60);

        // ---------------- DUE SOON ----------------

        if (diffHours > 0 && diffHours <= 4) {

            const taskName = card.querySelector("h3").innerText;

            showNotification(taskName);

        }

    });

});

// ---------------- SHOW NOTIFICATION ----------------

function showNotification(taskName) {

    if (Notification.permission === "granted") {

        new Notification("⏰ Aura Reminder", {

            body: `"${taskName}" is due soon!`,
            icon: "https://cdn-icons-png.flaticon.com/512/1827/1827392.png"

        });

    }

}