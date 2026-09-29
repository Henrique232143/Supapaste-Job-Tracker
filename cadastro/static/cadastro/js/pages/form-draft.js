document.addEventListener("DOMContentLoaded", () => {

    const form =
        document.querySelector("[data-draft-form]");


    if (!form) {
        return;
    }


    const themeUser =
        document.documentElement.dataset.themeUser ||
        "guest";


    const draftName =
        form.dataset.draftForm;


    const storageKey =
        `job-tracker-draft-${themeUser}-${draftName}`;


    const ignoredFields = new Set([
        "csrfmiddlewaretoken",
        "password",
        "senha",
        "confirmar_senha",
        "cpf"
    ]);


    function canSaveField(field) {

        if (!field.name) {
            return false;
        }


        if (ignoredFields.has(field.name)) {
            return false;
        }


        if (
            field.type === "password" ||
            field.type === "file" ||
            field.type === "submit" ||
            field.type === "button"
        ) {
            return false;
        }


        return true;

    }


    function saveDraft() {

        const draft = {};


        for (const field of form.elements) {

            if (!canSaveField(field)) {
                continue;
            }


            if (
                field.type === "checkbox" ||
                field.type === "radio"
            ) {

                draft[field.name] =
                    field.checked;

                continue;

            }


            draft[field.name] =
                field.value;

        }


        try {

            localStorage.setItem(
                storageKey,
                JSON.stringify(draft)
            );

        } catch {
            // Se o navegador bloquear localStorage,
            // o formulário continua funcionando normalmente.
        }

    }


    function restoreDraft() {

        let savedDraft;


        try {

            savedDraft =
                localStorage.getItem(storageKey);

        } catch {

            return;

        }


        if (!savedDraft) {
            return;
        }


        let draft;


        try {

            draft =
                JSON.parse(savedDraft);

        } catch {

            localStorage.removeItem(storageKey);

            return;

        }


        for (const field of form.elements) {

            if (!canSaveField(field)) {
                continue;
            }


            if (!(field.name in draft)) {
                continue;
            }


            if (
                field.type === "checkbox" ||
                field.type === "radio"
            ) {

                field.checked =
                    Boolean(draft[field.name]);

                continue;

            }


            /*
             * Não substitui um valor que o Django
             * já devolveu para o formulário.
             *
             * Isso é importante quando houve erro
             * de validação no backend.
             */

            if (!field.value) {

                field.value =
                    draft[field.name];

            }

        }

    }


    function clearDraft() {

        try {

            localStorage.removeItem(
                storageKey
            );

        } catch {
            // Nada precisa acontecer.
        }

    }


    /*
     * Recupera o rascunho assim que a página abre.
     */

    restoreDraft();


    /*
     * Salva sempre que algum campo for alterado.
     */

    form.addEventListener(
        "input",
        saveDraft
    );


    form.addEventListener(
        "change",
        saveDraft
    );


    /*
     * Não apagamos imediatamente no submit.
     *
     * Se o backend rejeitar o formulário por algum
     * erro, queremos continuar tendo o rascunho.
     */

    form.addEventListener(
        "submit",
        () => {

            sessionStorage.setItem(
                `${storageKey}-submitted`,
                "true"
            );

        }
    );


    /*
     * Permite que outra página avise que o cadastro
     * realmente foi concluído antes de apagar.
     */

    window.JobTrackerDraft = {

        clear() {
            clearDraft();
        },

        key: storageKey

    };

});