console.log("AURA SYSTEM ACTIVE");

// Browser notification permission
if (Notification.permission !== "granted") {
    Notification.requestPermission();
}

// Reminder popup
setTimeout(() => {

    if (Notification.permission === "granted") {

        new Notification("📌 Reminder", {
            body: "Check your upcoming tasks in AURA TODO!"
        });

    }

}, 5000);