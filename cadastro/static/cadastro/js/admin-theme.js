document.addEventListener("DOMContentLoaded", () => {

    const themeToggle = document.querySelector(".theme-toggle");

    if (!themeToggle) {
        return;
    }


    // =====================================================
    // TEMA INICIAL
    // =====================================================

    let savedTheme = localStorage.getItem("theme");


    // Se o Django tiver deixado "auto" ou qualquer outro
    // valor, começamos pelo modo claro.
    if (
        savedTheme !== "light" &&
        savedTheme !== "dark"
    ) {
        savedTheme = "light";
    }


    function applyTheme(theme) {

        document.documentElement.dataset.theme = theme;

        localStorage.setItem(
            "theme",
            theme
        );


        themeToggle.setAttribute(
            "aria-label",
            theme === "dark"
                ? "Ativar modo claro"
                : "Ativar modo escuro"
        );


        themeToggle.setAttribute(
            "title",
            theme === "dark"
                ? "Modo claro"
                : "Modo escuro"
        );

    }


    applyTheme(savedTheme);


    // =====================================================
    // TROCA DE TEMA
    // =====================================================

    themeToggle.addEventListener(
        "click",
        (event) => {

            /*
             Impede o evento padrão do Django Admin,
             que alternaria:

             auto → claro → escuro
            */

            event.preventDefault();

            event.stopImmediatePropagation();


            const currentTheme =
                document.documentElement.dataset.theme;


            const nextTheme =
                currentTheme === "dark"
                    ? "light"
                    : "dark";


            applyTheme(nextTheme);

        },
        true
    );

});