document.addEventListener("DOMContentLoaded", () => {

    /*
     * =====================================================
     * INTERAÇÃO DO MOCKUP
     * =====================================================
     *
     * O dashboard mostrado na landing acompanha
     * levemente o movimento do mouse.
     */


    const product =
        document.querySelector(".landing-product");


    const productWindow =
        document.querySelector(".product-window");


    /*
     * Se os elementos não existirem,
     * não fazemos nada.
     */

    if (
        !product ||
        !productWindow
    ) {
        return;
    }


    /*
     * Respeita a preferência do usuário
     * por menos movimento.
     */

    const reducedMotion =
        window.matchMedia(
            "(prefers-reduced-motion: reduce)"
        ).matches;


    if (reducedMotion) {
        return;
    }


    /*
     * Não aplicamos o efeito em telas menores.
     */

    if (window.innerWidth <= 900) {
        return;
    }


    /*
     * =====================================================
     * MOVIMENTO DO MOCKUP
     * =====================================================
     */

    product.addEventListener(
        "mousemove",
        (event) => {

            const rect =
                product.getBoundingClientRect();


            /*
             * Posição horizontal do mouse.
             *
             * 0 = esquerda
             * 0.5 = centro
             * 1 = direita
             */

            const x =
                (
                    event.clientX -
                    rect.left
                )
                /
                rect.width;


            /*
             * Posição vertical.
             */

            const y =
                (
                    event.clientY -
                    rect.top
                )
                /
                rect.height;


            /*
             * Transformamos a posição em
             * uma pequena rotação.
             */

            const rotateY =
                (x - 0.5) * 3;


            const rotateX =
                (0.5 - y) * 2;


            productWindow.style.transform =
                `
                rotateY(${rotateY}deg)
                rotateX(${rotateX}deg)
                translateY(-2px)
                `;

        }
    );


    /*
     * =====================================================
     * RETORNO AO ESTADO ORIGINAL
     * =====================================================
     */

    product.addEventListener(
        "mouseleave",
        () => {

            productWindow.style.transform =
                `
                rotateY(-3deg)
                rotateX(1deg)
                `;

        }
    );

});