document.addEventListener("DOMContentLoaded", () => {

    /*
     * =====================================================
     * LOADING GLOBAL
     * =====================================================
     */

    const loadingScreen =
        document.getElementById("loading-screen");


    function showLoading() {

        if (!loadingScreen) {
            return;
        }

        loadingScreen.classList.add("is-visible");

        loadingScreen.setAttribute(
            "aria-hidden",
            "false"
        );
    }


    function hideLoading() {

        if (!loadingScreen) {
            return;
        }

        loadingScreen.classList.remove("is-visible");

        loadingScreen.setAttribute(
            "aria-hidden",
            "true"
        );
    }


    /*
     * Deixa as funções disponíveis globalmente.
     */

    window.showLoading = showLoading;
    window.hideLoading = hideLoading;


    /*
     * =====================================================
     * PAGESHOW
     * =====================================================
     *
     * Garante que o loading seja removido quando
     * a nova página terminar de carregar.
     */

    window.addEventListener("pageshow", () => {

        hideLoading();

    });


    /*
     * =====================================================
     * PRELOAD
     * =====================================================
     *
     * Remove a classe inicial depois que a página
     * estiver pronta.
     */

    window.setTimeout(() => {

        document.body.classList.remove("is-preload");

    }, 80);


    /*
     * =====================================================
     * REVEAL
     * =====================================================
     */

    const revealElements =
        document.querySelectorAll(".reveal");


    if ("IntersectionObserver" in window) {

        const observer =
            new IntersectionObserver(
                (entries, observerInstance) => {

                    entries.forEach((entry) => {

                        if (!entry.isIntersecting) {
                            return;
                        }

                        entry.target.classList.add(
                            "is-visible"
                        );

                        observerInstance.unobserve(
                            entry.target
                        );

                    });

                },
                {
                    threshold: 0.12
                }
            );


        revealElements.forEach((element) => {

            observer.observe(element);

        });

    } else {

        revealElements.forEach((element) => {

            element.classList.add(
                "is-visible"
            );

        });

    }


    /*
     * =====================================================
     * NAVEGAÇÃO INTERNA
     * =====================================================
     */

    document.addEventListener(
        "click",
        (event) => {

            /*
             * Apenas clique principal.
             */

            if (event.button !== 0) {
                return;
            }


            /*
             * Não interferir em:
             *
             * Ctrl + clique
             * Shift + clique
             * Alt + clique
             * Cmd + clique
             */

            if (
                event.ctrlKey ||
                event.shiftKey ||
                event.altKey ||
                event.metaKey
            ) {
                return;
            }


            /*
             * Encontrar o link clicado.
             */

            const link =
                event.target.closest("a[href]");


            if (!link) {
                return;
            }


            const href =
                link.getAttribute("href");


            /*
             * Ignorar links especiais.
             */

            if (
                !href ||
                href === "#" ||
                href.startsWith("#") ||
                href.startsWith("mailto:") ||
                href.startsWith("tel:") ||
                href.startsWith("javascript:")
            ) {
                return;
            }


            /*
             * Não interferir em links que abrem
             * uma nova aba.
             */

            if (link.target === "_blank") {
                return;
            }


            /*
             * Não interferir em downloads.
             */

            if (link.hasAttribute("download")) {
                return;
            }


            let destination;


            try {

                destination =
                    new URL(
                        href,
                        window.location.href
                    );

            } catch {

                return;

            }


            /*
             * Apenas links internos.
             */

            if (
                destination.origin !==
                window.location.origin
            ) {
                return;
            }


            /*
             * Não fazer nada se já estivermos
             * exatamente na mesma URL.
             */

            if (
                destination.href ===
                window.location.href
            ) {
                return;
            }


            /*
             * Impede a navegação imediata.
             */

            event.preventDefault();


            /*
             * Mostra o loading.
             */

            showLoading();


            /*
             * Dois requestAnimationFrame dão ao navegador
             * tempo para realmente desenhar:
             *
             * - overlay
             * - blur
             * - spinner
             * - "Carregando"
             */

            window.requestAnimationFrame(() => {

                window.requestAnimationFrame(() => {

                    window.location.href =
                        destination.href;

                });

            });

        },
        true
    );


    /*
     * =====================================================
     * FORMULÁRIOS
     * =====================================================
     */

    document.addEventListener(
        "submit",
        (event) => {

            const form =
                event.target;


            if (
                !(form instanceof HTMLFormElement)
            ) {
                return;
            }


            /*
             * O evento submit só ocorre depois que
             * a validação nativa do navegador passou.
             */

            event.preventDefault();


            /*
             * Mostra o loading.
             */

            showLoading();


            /*
             * Aguarda o navegador desenhar
             * o overlay antes de enviar.
             */

            window.requestAnimationFrame(() => {

                window.requestAnimationFrame(() => {

                    HTMLFormElement.prototype.submit.call(
                        form
                    );

                });

            });

        },
        true
    );


    /*
     * =====================================================
     * EFEITO DE PRESSÃO DOS BOTÕES
     * =====================================================
     */

    const buttons =
        document.querySelectorAll(
            "button, .btn, .button"
        );


    buttons.forEach((button) => {

        button.addEventListener(
            "pointerdown",
            () => {

                button.classList.add(
                    "is-pressed"
                );

            }
        );


        button.addEventListener(
            "pointerup",
            () => {

                button.classList.remove(
                    "is-pressed"
                );

            }
        );


        button.addEventListener(
            "pointerleave",
            () => {

                button.classList.remove(
                    "is-pressed"
                );

            }
        );

    });

});