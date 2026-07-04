document.addEventListener("DOMContentLoaded", () => {

    if (!("Notification" in window)) {

        alert("Browser does not support notifications");

        return;

    }

    Notification.requestPermission().then(permission => {

        if (permission === "granted") {

            checkTasks();

        }

    });

});

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

            new Notification("⏰ Aura Reminder", {

                body: `${taskName} is due soon!`

            });

        }

    });

}