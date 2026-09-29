document.addEventListener("DOMContentLoaded", () => {

    const toggles = document.querySelectorAll(
        "[data-password-toggle]"
    );


    toggles.forEach((toggle) => {

        const targetId =
            toggle.dataset.passwordTarget;

        const input =
            document.getElementById(targetId);


        if (!input) {
            return;
        }


        toggle.addEventListener("click", () => {

            const mostrarSenha =
                input.type === "password";


            input.type =
                mostrarSenha
                    ? "text"
                    : "password";


            toggle.setAttribute(
                "aria-pressed",
                String(mostrarSenha)
            );


            toggle.setAttribute(
                "aria-label",
                mostrarSenha
                    ? "Ocultar senha"
                    : "Mostrar senha"
            );


            const iconEye =
                toggle.querySelector(
                    ".icon-eye"
                );


            const iconEyeOff =
                toggle.querySelector(
                    ".icon-eye-off"
                );


            if (iconEye) {

                iconEye.classList.toggle(
                    "is-hidden",
                    mostrarSenha
                );

            }


            if (iconEyeOff) {

                iconEyeOff.classList.toggle(
                    "is-hidden",
                    !mostrarSenha
                );

            }

        });

    });

});