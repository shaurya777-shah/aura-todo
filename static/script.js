document.addEventListener("DOMContentLoaded", () => {

    createNotificationButton();

    checkTasks();

});

function createNotificationButton() {

    if (!("Notification" in window)) {

        return;

    }

    if (Notification.permission === "granted") {

        return;

    }

    const btn = document.createElement("button");

    btn.innerText = "🔔 Enable Notifications";

    btn.style.position = "fixed";
    btn.style.bottom = "90px";
    btn.style.right = "20px";
    btn.style.padding = "14px 18px";
    btn.style.border = "none";
    btn.style.borderRadius = "18px";
    btn.style.background = "linear-gradient(135deg,#7c3aed,#ec4899)";
    btn.style.color = "white";
    btn.style.fontWeight = "bold";
    btn.style.cursor = "pointer";
    btn.style.zIndex = "9999";
    btn.style.boxShadow = "0 6px 20px rgba(0,0,0,0.15)";

    document.body.appendChild(btn);

    btn.addEventListener("click", () => {

        Notification.requestPermission().then(permission => {

            if (permission === "granted") {

                btn.remove();

                new Notification("✅ Notifications Enabled", {

                    body: "Aura reminders are now active!"

                });

            }

        });

    });

}

function checkTasks() {

    const taskCards = document.querySelectorAll(".task-card");

    taskCards.forEach(card => {

        const dueElement = card.querySelector(".due-time");

        if (!dueElement) return;

        const dueRaw = dueElement.dataset.raw;

        if (!dueRaw || dueRaw === "No Due Date") return;

        const dueDate = new Date(dueRaw);

        const now = new Date();

        const diffMs = dueDate - now;

        const diffHours = diffMs / (1000 * 60 * 60);

        if (diffHours > 0 && diffHours <= 4) {

            const taskName = card.querySelector("h3").innerText;

            if (Notification.permission === "granted") {

                new Notification("⏰ Aura Reminder", {

                    body: `${taskName} is due soon!`

                });

            }

        }

    });

}