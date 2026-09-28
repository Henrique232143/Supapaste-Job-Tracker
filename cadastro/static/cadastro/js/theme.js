document.addEventListener("DOMContentLoaded", () => {

    const themeToggle =
        document.getElementById("theme-toggle");

    if (!themeToggle) {
        return;
    }


    const icon =
        themeToggle.querySelector(".theme-toggle-icon");


    const themeUser =
        document.documentElement.dataset.themeUser ||
        "guest";


    const storageKey =
        `job-tracker-theme-${themeUser}`;


    function getCurrentTheme() {

        return (
            document.documentElement.dataset.theme ||
            "light"
        );

    }


    function updateButton(theme) {

        const isDark =
            theme === "dark";


        themeToggle.setAttribute(
            "aria-pressed",
            String(isDark)
        );


        themeToggle.setAttribute(
            "aria-label",
            isDark
                ? "Ativar modo claro"
                : "Ativar modo escuro"
        );


        if (icon) {

            icon.textContent =
                isDark
                    ? "\u2600"
                    : "\u263E";

        }

    }


    function applyTheme(theme) {

        document.documentElement.dataset.theme =
            theme;


        try {

            localStorage.setItem(
                storageKey,
                theme
            );

        } catch {
            // O navegador bloqueou o localStorage.
        }


        updateButton(theme);

    }


    const initialTheme =
        getCurrentTheme();


    updateButton(initialTheme);


    themeToggle.addEventListener(
        "click",
        () => {

            const currentTheme =
                getCurrentTheme();


            const nextTheme =
                currentTheme === "dark"
                    ? "light"
                    : "dark";


            applyTheme(nextTheme);

        }
    );

});