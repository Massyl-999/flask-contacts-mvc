/*
 * forms.js - Comportements communs aux formulaires.
 *  - form[data-validate] : validation côté client (mêmes règles que le serveur)
 *  - form[data-confirm]  : demande de confirmation avant l'envoi
 * La validation côté serveur reste la référence : ce script améliore seulement
 * le confort d'utilisation.
 */
(function () {
    "use strict";

    var MIN_NAME_LENGTH = 2;
    var PHONE_REGEX = /^[0-9]{10}$/;
    var EMAIL_REGEX = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

    document.querySelectorAll("form[data-validate]").forEach(function (form) {
        form.addEventListener("submit", function (event) {
            var value = function (name) {
                return form.elements[name].value.trim();
            };
            var errors = [];

            if (value("nom").length < MIN_NAME_LENGTH) {
                errors.push("Le nom doit contenir au moins " + MIN_NAME_LENGTH + " caractères");
            }
            if (value("prenom").length < MIN_NAME_LENGTH) {
                errors.push("Le prénom doit contenir au moins " + MIN_NAME_LENGTH + " caractères");
            }
            if (value("telephone") && !PHONE_REGEX.test(value("telephone"))) {
                errors.push("Le numéro de téléphone doit contenir 10 chiffres");
            }
            if (value("email") && !EMAIL_REGEX.test(value("email"))) {
                errors.push("Format d'email invalide");
            }

            if (errors.length > 0) {
                event.preventDefault();
                alert(errors.join("\n"));
            }
        });
    });

    document.querySelectorAll("form[data-confirm]").forEach(function (form) {
        form.addEventListener("submit", function (event) {
            if (!window.confirm(form.dataset.confirm)) {
                event.preventDefault();
            }
        });
    });
})();
